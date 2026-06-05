<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\ForumPost;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response;

class ForumController extends Controller
{
    public function index(Request $request): Response
    {
        $posts = ForumPost::query()
            ->with([
                'user',
                'comments.user',
            ])
            ->latest()
            ->get();

        return Inertia::render('Forum/Index', [
            'posts' => $posts,
        ]);
    }

    public function storePost(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'title' => ['required', 'string', 'max:255'],
            'content' => ['required', 'string', 'max:3000'],
        ]);

        ForumPost::create([
            'user_id' => $request->user()->id,
            'title' => strip_tags(trim($validated['title'])),
            'content' => strip_tags(trim($validated['content'])),
        ]);

        return back()->with('success', 'Postingan forum berhasil dibuat.');
    }

    public function storeComment(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'forum_post_id' => ['required', 'exists:forum_posts,id'],
            'content' => ['required', 'string', 'max:1000'],
        ]);

        Comment::create([
            'forum_post_id' => $validated['forum_post_id'],
            'user_id' => $request->user()->id,
            'content' => strip_tags(trim($validated['content'])),
        ]);

        return back()->with('success', 'Komentar berhasil ditambahkan.');
    }
}