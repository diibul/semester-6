<?php

namespace Tests\Feature;

use App\Models\Schedule;
use App\Models\Studio;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class Phase5EdgeCaseTest extends TestCase
{
    use RefreshDatabase;

    public function test_booking_is_rejected_when_schedule_is_unavailable(): void
    {
        $user = User::factory()->create();
        $studio = Studio::create([
            'name' => 'Studio Full',
            'slug' => 'studio-full',
            'type' => 'Rehearsal',
            'description' => 'Studio sudah penuh.',
            'location' => 'Bandung',
            'price_per_hour' => 100000,
        ]);

        $schedule = Schedule::create([
            'studio_id' => $studio->id,
            'schedule_date' => now()->addDay()->toDateString(),
            'start_time' => '09:00:00',
            'end_time' => '11:00:00',
            'is_available' => false,
        ]);

        $response = $this->actingAs($user)
            ->from('/studios/studio-full')
            ->post('/bookings', [
                'studio_id' => $studio->id,
                'schedule_id' => $schedule->id,
                'booking_date' => $schedule->schedule_date->toDateString(),
                'notes' => 'Coba booking',
            ]);

        $response->assertRedirect('/studios/studio-full');
        $response->assertSessionHasErrors('schedule_id');
    }

    public function test_booking_and_forum_validate_required_input(): void
    {
        $user = User::factory()->create();

        $bookingResponse = $this->actingAs($user)->post('/bookings', []);
        $bookingResponse->assertSessionHasErrors([
            'studio_id',
            'schedule_id',
            'booking_date',
        ]);

        $postResponse = $this->actingAs($user)->post('/forum/posts', [
            'title' => '',
            'content' => '',
        ]);

        $postResponse->assertSessionHasErrors(['title', 'content']);
    }

    public function test_sql_injection_like_input_does_not_authenticate(): void
    {
        User::factory()->create([
            'email' => 'safe@example.com',
            'password' => 'password',
        ]);

        $this->post('/login', [
            'email' => "' OR 1=1 --",
            'password' => "' OR 1=1 --",
        ]);

        $this->assertGuest();
    }

    public function test_forum_rejects_oversized_spam_like_payload(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->post('/forum/posts', [
            'title' => str_repeat('x', 400),
            'content' => str_repeat('spam ', 1000),
        ]);

        $response->assertSessionHasErrors(['title', 'content']);
    }
}
