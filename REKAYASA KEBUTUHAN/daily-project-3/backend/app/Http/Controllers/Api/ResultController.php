<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\TrackingResult;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class ResultController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $results = TrackingResult::query()
            ->with('alumni:id,name,nim,study_program,tracking_status')
            ->latest('created_at')
            ->paginate((int) $request->query('per_page', 10));

        return response()->json($results);
    }

    public function show(TrackingResult $result): JsonResponse
    {
        $result->load('alumni:id,name,nim,study_program,tracking_status');

        return response()->json($result);
    }

    public function verify(Request $request, TrackingResult $result): JsonResponse
    {
        $validated = $request->validate([
            'action' => ['required', 'in:confirm,uncertain,invalid'],
        ]);

        $mapping = [
            'confirm' => 'Teridentifikasi',
            'uncertain' => 'Perlu Verifikasi',
            'invalid' => 'Belum Ditemukan',
        ];

        $newStatus = $mapping[$validated['action']];

        $result->update([
            'status' => $newStatus,
        ]);

        $result->alumni()->update([
            'tracking_status' => $newStatus,
        ]);

        return response()->json([
            'message' => 'Status hasil tracking berhasil diperbarui.',
            'result' => $result->fresh('alumni:id,name,nim,study_program,tracking_status'),
        ]);
    }
}
