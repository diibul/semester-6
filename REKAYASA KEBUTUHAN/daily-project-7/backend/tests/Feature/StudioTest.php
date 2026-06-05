<?php

namespace Tests\Feature;

use App\Models\Schedule;
use App\Models\Studio;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class StudioTest extends TestCase
{
    use RefreshDatabase;

    public function test_studio_pages_can_be_rendered(): void
    {
        $studio = Studio::create([
            'name' => 'Studio Test',
            'slug' => 'studio-test',
            'type' => 'Rehearsal',
            'description' => 'Deskripsi studio test.',
            'location' => 'Bandung',
            'price_per_hour' => 100000,
        ]);

        Schedule::create([
            'studio_id' => $studio->id,
            'schedule_date' => now()->addDay()->toDateString(),
            'start_time' => '10:00:00',
            'end_time' => '12:00:00',
            'is_available' => true,
        ]);

        $this->get('/studios')->assertOk();
        $this->get('/studios/studio-test')->assertOk();
    }

    public function test_owner_can_create_update_delete_studio_and_generate_schedule(): void
    {
        $owner = User::factory()->create();

        $createResponse = $this->actingAs($owner)->post('/studios', [
            'name' => 'Studio Baru',
            'type' => 'Rehearsal',
            'description' => 'Studio baru untuk test.',
            'location' => 'Bandung',
            'price_per_hour' => 110000,
        ]);

        $createResponse->assertRedirect();

        $studio = Studio::query()->where('name', 'Studio Baru')->firstOrFail();
        $this->assertSame($owner->id, $studio->user_id);

        $this->actingAs($owner)->patch('/studios/'.$studio->slug, [
            'name' => 'Studio Baru Update',
            'type' => 'Recording',
            'description' => 'Update studio.',
            'location' => 'Jakarta',
            'price_per_hour' => 150000,
        ])->assertRedirect();

        $studio->refresh();
        $this->assertSame('Studio Baru Update', $studio->name);

        $this->actingAs($owner)->post('/studios/'.$studio->slug.'/schedules', [
            'schedule_date' => now()->addDay()->toDateString(),
            'start_time' => '10:00',
            'end_time' => '12:00',
        ])->assertRedirect();

        $this->assertDatabaseHas('schedules', [
            'studio_id' => $studio->id,
            'start_time' => '10:00:00',
            'end_time' => '12:00:00',
            'is_available' => 1,
        ]);

        $this->actingAs($owner)->delete('/studios/'.$studio->slug)->assertRedirect('/studios');

        $this->assertDatabaseMissing('studios', [
            'id' => $studio->id,
        ]);
    }

    public function test_non_owner_cannot_modify_studio(): void
    {
        $owner = User::factory()->create();
        $otherUser = User::factory()->create();

        $studio = Studio::create([
            'user_id' => $owner->id,
            'name' => 'Studio Private',
            'slug' => 'studio-private',
            'type' => 'Rehearsal',
            'description' => 'Studio milik owner.',
            'location' => 'Bandung',
            'price_per_hour' => 100000,
        ]);

        $this->actingAs($otherUser)->patch('/studios/'.$studio->slug, [
            'name' => 'Studio Hack',
            'type' => 'Rehearsal',
            'description' => 'x',
            'location' => 'x',
            'price_per_hour' => 1,
        ])->assertForbidden();

        $this->actingAs($otherUser)->delete('/studios/'.$studio->slug)->assertForbidden();
        $this->actingAs($otherUser)->post('/studios/'.$studio->slug.'/schedules', [
            'schedule_date' => now()->addDay()->toDateString(),
            'start_time' => '10:00',
            'end_time' => '12:00',
        ])->assertForbidden();
    }
}
