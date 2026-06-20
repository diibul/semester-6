<?php

namespace App\Http\Controllers;

use App\Models\Schedule;
use App\Models\Studio;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use Illuminate\Validation\ValidationException;
use Inertia\Inertia;
use Inertia\Response;

class StudioController extends Controller
{
    public function index(): Response
    {
        $studios = Studio::query()
            ->with(['schedules' => function ($query) {
                $query->orderBy('schedule_date')->orderBy('start_time');
            }])
            ->latest()
            ->get();

        return Inertia::render('Studios/Index', [
            'studios' => $studios,
        ]);
    }

    public function show(Studio $studio): Response
    {
        $studio->load([
            'schedules' => function ($query) {
                $query->with('booking')
                    ->orderBy('schedule_date')
                    ->orderBy('start_time');
            },
        ]);

        return Inertia::render('Studios/Show', [
            'studio' => $studio,
        ]);
    }

    public function store(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'slug' => ['nullable', 'string', 'max:255', 'alpha_dash', 'unique:studios,slug'],
            'type' => ['required', 'string', 'max:100'],
            'description' => ['required', 'string', 'max:3000'],
            'location' => ['required', 'string', 'max:255'],
            'price_per_hour' => ['required', 'numeric', 'min:0'],
            'image_url' => ['nullable', 'url', 'max:2000'],
        ]);

        $slug = $validated['slug'] ?? Str::slug($validated['name']);

        Studio::create([
            'user_id' => $request->user()->id,
            'name' => trim($validated['name']),
            'slug' => $slug,
            'type' => trim($validated['type']),
            'description' => trim($validated['description']),
            'location' => trim($validated['location']),
            'price_per_hour' => $validated['price_per_hour'],
            'image_url' => $validated['image_url'] ?? null,
        ]);

        return back()->with('success', 'Studio berhasil dibuat.');
    }

    public function update(Request $request, Studio $studio): RedirectResponse
    {
        $this->authorizeOwner($request, $studio);

        $validated = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'slug' => ['nullable', 'string', 'max:255', 'alpha_dash', Rule::unique('studios', 'slug')->ignore($studio->id)],
            'type' => ['required', 'string', 'max:100'],
            'description' => ['required', 'string', 'max:3000'],
            'location' => ['required', 'string', 'max:255'],
            'price_per_hour' => ['required', 'numeric', 'min:0'],
            'image_url' => ['nullable', 'url', 'max:2000'],
        ]);

        $studio->update([
            'name' => trim($validated['name']),
            'slug' => $validated['slug'] ?? Str::slug($validated['name']),
            'type' => trim($validated['type']),
            'description' => trim($validated['description']),
            'location' => trim($validated['location']),
            'price_per_hour' => $validated['price_per_hour'],
            'image_url' => $validated['image_url'] ?? null,
        ]);

        return back()->with('success', 'Studio berhasil diperbarui.');
    }

    public function destroy(Request $request, Studio $studio): RedirectResponse
    {
        $this->authorizeOwner($request, $studio);

        $studio->delete();

        return redirect()->route('studios.index')->with('success', 'Studio berhasil dihapus.');
    }

    public function storeSchedule(Request $request, Studio $studio): RedirectResponse
    {
        $this->authorizeOwner($request, $studio);

        $validated = $request->validate([
            'schedule_date' => ['required', 'date'],
            'start_time' => ['required', 'date_format:H:i'],
            'end_time' => ['required', 'date_format:H:i', 'after:start_time'],
        ]);

        $exists = Schedule::query()
            ->where('studio_id', $studio->id)
            ->where('schedule_date', $validated['schedule_date'])
            ->where('start_time', $validated['start_time'].':00')
            ->where('end_time', $validated['end_time'].':00')
            ->exists();

        if ($exists) {
            throw ValidationException::withMessages([
                'schedule' => 'Jadwal ini sudah ada.',
            ]);
        }

        Schedule::create([
            'studio_id' => $studio->id,
            'schedule_date' => $validated['schedule_date'],
            'start_time' => $validated['start_time'].':00',
            'end_time' => $validated['end_time'].':00',
            'is_available' => true,
        ]);

        return back()->with('success', 'Jadwal berhasil ditambahkan.');
    }

    private function authorizeOwner(Request $request, Studio $studio): void
    {
        // Legacy studios without owner are treated as locked for modification.
        if ($studio->user_id === null) {
            abort(403);
        }

        abort_unless((int) $studio->user_id === (int) $request->user()->id, 403);
    }
}
