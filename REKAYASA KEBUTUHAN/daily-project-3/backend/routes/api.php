<?php

use App\Http\Controllers\Api\AlumniController;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\DashboardController;
use App\Http\Controllers\Api\ResultController;
use App\Http\Controllers\Api\TrackingController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/login', function (Request $request) {
    return response()->json(['message' => 'Unauthenticated.'], 401);
})->name('login');

Route::post('/login', [AuthController::class, 'login'])->name('auth.login');

Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/me', [AuthController::class, 'me']);

    Route::get('/dashboard', [DashboardController::class, 'index']);

    Route::get('/alumni', [AlumniController::class, 'index']);
    Route::post('/alumni', [AlumniController::class, 'store']);
    Route::get('/alumni/{alumni}', [AlumniController::class, 'show']);
    Route::put('/alumni/{alumni}', [AlumniController::class, 'update']);
    Route::delete('/alumni/{alumni}', [AlumniController::class, 'destroy']);

    Route::post('/tracking/{alumni}', [TrackingController::class, 'run']);

    Route::get('/results', [ResultController::class, 'index']);
    Route::get('/results/{result}', [ResultController::class, 'show']);
    Route::put('/results/{result}/verify', [ResultController::class, 'verify']);
});
