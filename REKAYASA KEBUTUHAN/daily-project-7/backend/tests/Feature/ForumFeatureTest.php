<?php

namespace Tests\Feature;

use App\Models\ForumPost;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ForumFeatureTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_post_and_comment(): void
    {
        $user = User::factory()->create();

        $postResponse = $this->actingAs($user)->post('/forum/posts', [
            'title' => '<b>Acoustic Session</b>',
            'content' => '<script>alert(1)</script>Diskusi gear band.',
        ]);

        $postResponse->assertRedirect();

        $post = ForumPost::query()->firstOrFail();

        $this->assertSame('Acoustic Session', $post->title);
        $this->assertSame('alert(1)Diskusi gear band.', $post->content);

        $commentResponse = $this->actingAs($user)->post('/forum/comments', [
            'forum_post_id' => $post->id,
            'content' => '<i>Nice discussion</i>',
        ]);

        $commentResponse->assertRedirect();

        $this->assertDatabaseHas('comments', [
            'forum_post_id' => $post->id,
            'user_id' => $user->id,
            'content' => 'Nice discussion',
        ]);
    }

    public function test_forum_page_can_be_rendered(): void
    {
        $user = User::factory()->create();

        $this->actingAs($user)->get('/forum')->assertOk();
    }
}