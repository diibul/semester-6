<?php

namespace Tests\Feature;

use App\Models\Booking;
use App\Models\Schedule;
use App\Models\Studio;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class BookingFeatureTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_book_a_schedule_and_double_booking_is_blocked(): void
    {
        $user = User::factory()->create();
        $studio = Studio::create([
            'name' => 'Studio Harmoni',
            'slug' => 'studio-harmoni',
            'type' => 'Rehearsal',
            'description' => 'Studio untuk latihan band.',
            'location' => 'Bandung',
            'price_per_hour' => 125000,
        ]);

        $schedule = Schedule::create([
            'studio_id' => $studio->id,
            'schedule_date' => now()->addDay()->toDateString(),
            'start_time' => '10:00:00',
            'end_time' => '12:00:00',
            'is_available' => true,
        ]);

        $response = $this->actingAs($user)->post('/bookings', [
            'studio_id' => $studio->id,
            'schedule_id' => $schedule->id,
            'booking_date' => $schedule->schedule_date->toDateString(),
            'notes' => '<b>Latihan band</b>',
        ]);

        $response->assertRedirect(route('bookings.index', absolute: false));

        $this->assertDatabaseHas('bookings', [
            'user_id' => $user->id,
            'studio_id' => $studio->id,
            'schedule_id' => $schedule->id,
            'booking_status' => 'pending',
            'payment_status' => 'unpaid',
            'notes' => 'Latihan band',
        ]);

        $otherUser = User::factory()->create();

        $doubleBookingResponse = $this
            ->actingAs($otherUser)
            ->from('/studios/studio-harmoni')
            ->post('/bookings', [
                'studio_id' => $studio->id,
                'schedule_id' => $schedule->id,
                'booking_date' => $schedule->schedule_date->toDateString(),
                'notes' => 'Coba booking lagi',
            ]);

        $doubleBookingResponse->assertRedirect('/studios/studio-harmoni');
        $doubleBookingResponse->assertSessionHasErrors('schedule_id');
        $this->assertDatabaseCount('bookings', 1);
    }

    public function test_user_can_mark_booking_paid_and_confirm_it(): void
    {
        $user = User::factory()->create();
        $studio = Studio::create([
            'user_id' => $user->id,
            'name' => 'Studio Resonansi',
            'slug' => 'studio-resonansi',
            'type' => 'Recording',
            'description' => 'Studio rekaman.',
            'location' => 'Jakarta',
            'price_per_hour' => 180000,
        ]);

        $schedule = Schedule::create([
            'studio_id' => $studio->id,
            'schedule_date' => now()->addDay()->toDateString(),
            'start_time' => '13:00:00',
            'end_time' => '15:00:00',
            'is_available' => false,
        ]);

        $booking = Booking::create([
            'user_id' => $user->id,
            'studio_id' => $studio->id,
            'schedule_id' => $schedule->id,
            'booking_date' => $schedule->schedule_date->toDateString(),
            'booking_status' => 'pending',
            'payment_status' => 'unpaid',
            'total_amount' => 180000,
            'notes' => 'Demo',
        ]);

        $this->actingAs($user)->post('/bookings/'.$booking->id.'/pay')
            ->assertRedirect();

        $this->assertDatabaseHas('bookings', [
            'id' => $booking->id,
            'booking_status' => 'paid',
            'payment_status' => 'paid',
        ]);

        $this->actingAs($user)->post('/bookings/'.$booking->id.'/confirm')
            ->assertRedirect();

        $this->assertDatabaseHas('bookings', [
            'id' => $booking->id,
            'booking_status' => 'confirmed',
            'payment_status' => 'paid',
        ]);
    }

    public function test_only_studio_owner_can_confirm_booking_when_owner_exists(): void
    {
        $owner = User::factory()->create();
        $booker = User::factory()->create();

        $studio = Studio::create([
            'user_id' => $owner->id,
            'name' => 'Studio Owner Only',
            'slug' => 'studio-owner-only',
            'type' => 'Recording',
            'description' => 'Studio rekaman.',
            'location' => 'Jakarta',
            'price_per_hour' => 180000,
        ]);

        $schedule = Schedule::create([
            'studio_id' => $studio->id,
            'schedule_date' => now()->addDay()->toDateString(),
            'start_time' => '13:00:00',
            'end_time' => '15:00:00',
            'is_available' => false,
        ]);

        $booking = Booking::create([
            'user_id' => $booker->id,
            'studio_id' => $studio->id,
            'schedule_id' => $schedule->id,
            'booking_date' => $schedule->schedule_date->toDateString(),
            'booking_status' => 'paid',
            'payment_status' => 'paid',
            'total_amount' => 180000,
        ]);

        $this->actingAs($booker)->post('/bookings/'.$booking->id.'/confirm')->assertForbidden();
        $this->actingAs($owner)->post('/bookings/'.$booking->id.'/confirm')->assertRedirect();

        $this->assertDatabaseHas('bookings', [
            'id' => $booking->id,
            'booking_status' => 'confirmed',
        ]);
    }
}
