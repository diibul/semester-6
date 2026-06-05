import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import { Head, Link, router, usePage } from '@inertiajs/react';
import { useState } from 'react';

export default function Index({ bookings }) {
    const flash = usePage().props.flash;
    const formatDate = (value) => String(value).slice(0, 10);
    const [processingAction, setProcessingAction] = useState(null);

    const runAction = (type, bookingId) => {
        const key = `${type}-${bookingId}`;
        setProcessingAction(key);

        router.post(route(`bookings.${type}`, bookingId), {}, {
            preserveScroll: true,
            onFinish: () => setProcessingAction(null),
        });
    };

    return (
        <AuthenticatedLayout
            header={<h2 className="text-xl font-semibold leading-tight text-gray-800">My Bookings</h2>}
        >
            <Head title="My Bookings" />

            <div className="py-12">
                <div className="mx-auto max-w-7xl space-y-6 px-4 sm:px-6 lg:px-8">
                    {flash.success && (
                        <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
                            {flash.success}
                        </div>
                    )}

                    {flash.error && (
                        <div className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
                            {flash.error}
                        </div>
                    )}

                    {bookings.length === 0 ? (
                        <div className="rounded-2xl bg-white p-8 shadow-sm">
                            <p className="text-gray-700">Belum ada booking. Silakan pilih studio dari halaman Studios.</p>
                            <Link href={route('studios.index')} className="mt-4 inline-flex rounded-md bg-gray-900 px-4 py-2 text-white">
                                Lihat studio
                            </Link>
                        </div>
                    ) : (
                        <div className="grid gap-4">
                            {bookings.map((booking) => (
                                <div key={booking.id} className="rounded-2xl bg-white p-6 shadow-sm">
                                    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                                        <div>
                                            <h3 className="text-lg font-semibold text-gray-900">{booking.studio.name}</h3>
                                            <p className="text-sm text-gray-600">
                                                {formatDate(booking.schedule.schedule_date)} | {booking.schedule.start_time} - {booking.schedule.end_time}
                                            </p>
                                            <p className="mt-2 text-sm text-gray-600">Status booking: {booking.booking_status}</p>
                                            <p className="text-sm text-gray-600">Status payment: {booking.payment_status}</p>
                                            {booking.notes && <p className="mt-2 text-sm text-gray-500">Catatan: {booking.notes}</p>}
                                        </div>

                                        <div className="flex flex-wrap gap-2">
                                            {(() => {
                                                const isPaid = booking.payment_status === 'paid';
                                                const isConfirmed = booking.booking_status === 'confirmed';
                                                const payDisabled = processingAction !== null || isPaid;
                                                const confirmDisabled = processingAction !== null || !isPaid || isConfirmed;

                                                return (
                                                    <>
                                            <button
                                                type="button"
                                                onClick={() => runAction('pay', booking.id)}
                                                disabled={payDisabled}
                                                className="rounded-md bg-amber-500 px-4 py-2 text-sm font-medium text-white hover:bg-amber-600 disabled:cursor-not-allowed disabled:opacity-60"
                                            >
                                                {processingAction === `pay-${booking.id}` ? 'Memproses...' : 'Dummy Payment'}
                                            </button>
                                            <button
                                                type="button"
                                                onClick={() => runAction('confirm', booking.id)}
                                                disabled={confirmDisabled}
                                                className="rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60"
                                            >
                                                {processingAction === `confirm-${booking.id}` ? 'Memproses...' : 'Confirm'}
                                            </button>
                                                    </>
                                                );
                                            })()}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </AuthenticatedLayout>
    );
}