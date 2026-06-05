<?php

namespace Database\Seeders;

use App\Models\Schedule;
use App\Models\Studio;
use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        $owner = User::factory()->create([
            'name' => 'Test User',
            'email' => 'test@example.com',
        ]);

        $studios = [
            [
                'user_id' => $owner->id,
                'name' => 'Studio Harmoni',
                'slug' => 'studio-harmoni',
                'type' => 'Rehearsal',
                'description' => 'Studio latihan band dengan akustik bersih, drum set lengkap, dan ruang nyaman.',
                'location' => 'Bandung',
                'price_per_hour' => 120000,
                'image_url' => null,
            ],
            [
                'user_id' => $owner->id,
                'name' => 'Studio Resonansi',
                'slug' => 'studio-resonansi',
                'type' => 'Recording',
                'description' => 'Studio rekaman sederhana untuk demo lagu, podcast, dan produksi konten musik.',
                'location' => 'Jakarta',
                'price_per_hour' => 180000,
                'image_url' => null,
            ],
            [
                'user_id' => $owner->id,
                'name' => 'Studio Nada Biru',
                'slug' => 'studio-nada-biru',
                'type' => 'Rehearsal',
                'description' => 'Ruangan latihan dengan sound system modern, cocok untuk komunitas dan band indie.',
                'location' => 'Yogyakarta',
                'price_per_hour' => 150000,
                'image_url' => null,
            ],
        ];

        foreach ($studios as $studioData) {
            $studio = Studio::create($studioData);

            foreach ([1, 2, 3] as $dayOffset) {
                Schedule::create([
                    'studio_id' => $studio->id,
                    'schedule_date' => now()->addDays($dayOffset)->toDateString(),
                    'start_time' => '10:00:00',
                    'end_time' => '12:00:00',
                    'is_available' => true,
                ]);

                Schedule::create([
                    'studio_id' => $studio->id,
                    'schedule_date' => now()->addDays($dayOffset)->toDateString(),
                    'start_time' => '13:00:00',
                    'end_time' => '15:00:00',
                    'is_available' => true,
                ]);
            }
        }
    }
}
