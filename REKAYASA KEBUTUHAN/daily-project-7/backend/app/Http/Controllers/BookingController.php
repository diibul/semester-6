<?php

namespace App\Http\Controllers;

use App\Models\Booking;
use App\Models\Schedule;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;
use Inertia\Inertia;
use Inertia\Response;

class BookingController extends Controller
{
    public function index(Request $request): Response
    {
        $bookings = Booking::query()
            ->with(['studio', 'schedule'])
            ->where('user_id', $request->user()->id)
            ->latest()
            ->get();

        return Inertia::render('Booking/Index', [
            'bookings' => $bookings,
        ]);
    }

    public function store(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'studio_id' => ['required', 'exists:studios,id'],
            'schedule_id' => ['required', 'exists:schedules,id'],
            'booking_date' => ['required', 'date'],
            'notes' => ['nullable', 'string', 'max:1000'],
        ]);

        $booking = DB::transaction(function () use ($request, $validated) {
            $schedule = Schedule::query()
                ->with('studio')
                ->whereKey($validated['schedule_id'])
                ->lockForUpdate()
                ->firstOrFail();

            if ((int) $schedule->studio_id !== (int) $validated['studio_id']) {
                throw ValidationException::withMessages([
                    'schedule_id' => 'Schedule tidak sesuai dengan studio yang dipilih.',
                ]);
            }

            if (! $schedule->is_available || $schedule->booking()->lockForUpdate()->exists()) {
                throw ValidationException::withMessages([
                    'schedule_id' => 'Jadwal ini sudah dibooking.',
                ]);
            }

            if ($schedule->schedule_date->toDateString() !== $validated['booking_date']) {
                throw ValidationException::withMessages([
                    'booking_date' => 'Tanggal booking harus sama dengan tanggal jadwal.',
                ]);
            }

            $booking = Booking::create([
                'user_id' => $request->user()->id,
                'studio_id' => $validated['studio_id'],
                'schedule_id' => $schedule->id,
                'booking_date' => $validated['booking_date'],
                'booking_status' => 'pending',
                'payment_status' => 'unpaid',
                'total_amount' => $schedule->studio->price_per_hour,
                'notes' => strip_tags(trim((string) ($validated['notes'] ?? ''))),
            ]);

            $schedule->update(['is_available' => false]);

            return $booking;
        }, 3);

        return redirect()
            ->route('bookings.index')
            ->with('success', 'Booking berhasil dibuat dengan status pending.');
    }

    public function pay(Request $request, Booking $booking): RedirectResponse
    {
        $this->authorizeOwner($request, $booking);

        if ($booking->payment_status === 'paid') {
            return back()->with('success', 'Booking sudah dibayar.');
        }

        $booking->update([
            'payment_status' => 'paid',
            'booking_status' => 'paid',
        ]);

        return back()->with('success', 'Pembayaran dummy berhasil.');
    }

    public function confirm(Request $request, Booking $booking): RedirectResponse
    {
        $this->authorizeApprovalOwner($request, $booking);

        if ($booking->payment_status !== 'paid') {
            throw ValidationException::withMessages([
                'booking' => 'Booking harus dibayar terlebih dahulu sebelum dikonfirmasi.',
            ]);
        }

        $booking->update([
            'booking_status' => 'confirmed',
        ]);

        return back()->with('success', 'Booking berhasil dikonfirmasi.');
    }

    private function authorizeOwner(Request $request, Booking $booking): void
    {
        abort_unless($booking->user_id === $request->user()->id, 403);
    }

    private function authorizeApprovalOwner(Request $request, Booking $booking): void
    {
        $booking->loadMissing('studio');

        // If studio has explicit owner, only owner can approve.
        if ($booking->studio?->user_id !== null) {
            abort_unless((int) $booking->studio->user_id === (int) $request->user()->id, 403);

            return;
        }

        // Backward compatibility for legacy records without studio owner.
        $this->authorizeOwner($request, $booking);
    }
}
