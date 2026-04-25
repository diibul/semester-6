<?php

use App\Http\Controllers\BookingController;
use App\Http\Controllers\ForumController;
use App\Http\Controllers\ProfileController;
use App\Http\Controllers\StudioController;
use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;

Route::get('/', function () {
    return Inertia::render('Welcome', [
        'canLogin' => Route::has('login'),
        'canRegister' => Route::has('register'),
        'laravelVersion' => Application::VERSION,
        'phpVersion' => PHP_VERSION,
    ]);
});

Route::get('/dashboard', function () {
    return Inertia::render('Dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

Route::get('/studios', [StudioController::class, 'index'])->name('studios.index');
Route::get('/studios/{studio:slug}', [StudioController::class, 'show'])->name('studios.show');

Route::middleware('auth')->group(function () {
    Route::post('/studios', [StudioController::class, 'store'])->name('studios.store');
    Route::patch('/studios/{studio:slug}', [StudioController::class, 'update'])->name('studios.update');
    Route::delete('/studios/{studio:slug}', [StudioController::class, 'destroy'])->name('studios.destroy');
    Route::post('/studios/{studio:slug}/schedules', [StudioController::class, 'storeSchedule'])->name('studios.schedules.store');

    Route::get('/bookings', [BookingController::class, 'index'])->name('bookings.index');
    Route::post('/bookings', [BookingController::class, 'store'])->name('bookings.store');
    Route::post('/bookings/{booking}/pay', [BookingController::class, 'pay'])->name('bookings.pay');
    Route::post('/bookings/{booking}/confirm', [BookingController::class, 'confirm'])->name('bookings.confirm');

    Route::get('/forum', [ForumController::class, 'index'])->name('forum.index');
    Route::post('/forum/posts', [ForumController::class, 'storePost'])->name('forum.posts.store');
    Route::post('/forum/comments', [ForumController::class, 'storeComment'])->name('forum.comments.store');

    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

require __DIR__.'/auth.php';
