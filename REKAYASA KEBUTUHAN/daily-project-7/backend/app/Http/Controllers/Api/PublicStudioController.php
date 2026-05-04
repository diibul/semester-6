<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Studio;
use Illuminate\Http\JsonResponse;

class PublicStudioController extends Controller
{
    public function index(): JsonResponse
    {
        $studios = Studio::query()
            ->withCount(['schedules as available_schedules_count' => function ($query) {
                $query->where('is_available', true);
            }])
            ->with(['schedules' => function ($query) {
                $query->where('is_available', true)
                    ->orderBy('schedule_date')
                    ->orderBy('start_time');
            }])
            ->latest()
            ->get();

        return response()->json([
            'data' => $studios,
        ]);
    }

    public function show(Studio $studio): JsonResponse
    {
        $studio->load([
            'schedules' => function ($query) {
                $query->where('is_available', true)
                    ->orderBy('schedule_date')
                    ->orderBy('start_time');
            },
        ]);

        return response()->json([
            'data' => $studio,
        ]);
    }
}
