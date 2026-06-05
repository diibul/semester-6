<?php

namespace Tests\Feature;

use App\Models\Comment;
use App\Models\ForumPost;
use App\Models\Schedule;
use App\Models\Studio;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class PerformanceQueryTest extends TestCase
{
    use RefreshDatabase;

    public function test_studio_index_uses_bounded_schedule_queries(): void
    {
        $this->seedStudiosWithSchedules();

        DB::flushQueryLog();
        DB::enableQueryLog();

        $this->get('/studios')->assertOk();

        $queries = collect(DB::getQueryLog());
        $scheduleQueries = $queries->filter(function (array $query) {
            $sql = strtolower($query['query']);

            return str_contains($sql, 'from "schedules"')
                || str_contains($sql, 'from `schedules`')
                || str_contains($sql, 'from schedules');
        })->count();

        $this->assertLessThanOrEqual(2, $scheduleQueries);
    }

    public function test_forum_index_uses_eager_loading_without_lazy_loading_errors(): void
    {
        $user = User::factory()->create();

        $post = ForumPost::create([
            'user_id' => $user->id,
            'title' => 'Post performance',
            'content' => 'Konten performance test',
        ]);

        Comment::create([
            'forum_post_id' => $post->id,
            'user_id' => $user->id,
            'content' => 'Komentar pertama',
        ]);

        \Illuminate\Database\Eloquent\Model::preventLazyLoading(true);

        try {
            $this->actingAs($user)->get('/forum')->assertOk();
        } finally {
            \Illuminate\Database\Eloquent\Model::preventLazyLoading(false);
        }
    }

    private function seedStudiosWithSchedules(): void
    {
        for ($i = 1; $i <= 5; $i++) {
            $studio = Studio::create([
                'name' => 'Studio '.$i,
                'slug' => 'studio-'.$i,
                'type' => 'Rehearsal',
                'description' => 'Studio ke '.$i,
                'location' => 'Bandung',
                'price_per_hour' => 100000 + ($i * 1000),
            ]);

            Schedule::create([
                'studio_id' => $studio->id,
                'schedule_date' => now()->addDays($i)->toDateString(),
                'start_time' => '10:00:00',
                'end_time' => '12:00:00',
                'is_available' => true,
            ]);
        }
    }
}
