<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Alumni;
use App\Models\TrackingResult;
use App\Services\TrackingSimulationService;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\DB;

class TrackingController extends Controller
{
    public function __construct(private readonly TrackingSimulationService $trackingSimulationService)
    {
    }

    public function run(Alumni $alumni): JsonResponse
    {
        $simulation = $this->trackingSimulationService->simulate($alumni);

        $savedResults = DB::transaction(function () use ($alumni, $simulation) {
            $createdResults = [];

            foreach ($simulation['candidates'] as $candidate) {
                $createdResults[] = TrackingResult::create([
                    'alumni_id' => $alumni->id,
                    'source' => $candidate['source'],
                    'title' => $candidate['title'],
                    'description' => $candidate['description'],
                    'url' => $candidate['url'],
                    'confidence_score' => $candidate['confidence_score'],
                    'status' => 'Perlu Verifikasi',
                    'tracked_at' => now(),
                    'created_at' => now(),
                ]);
            }

            $alumni->update([
                'tracking_status' => 'Perlu Verifikasi',
            ]);

            return $createdResults;
        });

        return response()->json([
            'message' => 'Tracking simulation selesai.',
            'queries' => $simulation['queries'],
            'results' => $savedResults,
        ]);
    }
}
