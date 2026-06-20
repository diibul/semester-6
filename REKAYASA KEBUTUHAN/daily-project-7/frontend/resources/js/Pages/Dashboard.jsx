import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import { Head, Link } from '@inertiajs/react';

export default function Dashboard() {
    return (
        <AuthenticatedLayout
            header={
                <h2 className="text-xl font-semibold leading-tight text-gray-800">
                    Dashboard
                </h2>
            }
        >
            <Head title="Dashboard" />

            <div className="py-12">
                <div className="mx-auto max-w-7xl space-y-6 px-4 sm:px-6 lg:px-8">
                    <div className="rounded-2xl bg-white p-6 shadow-sm">
                        <h3 className="text-lg font-semibold text-gray-900">Selamat datang</h3>
                        <p className="mt-2 text-gray-600">Pilih studio, lakukan booking, lalu lanjutkan diskusi di forum komunitas.</p>
                    </div>

                    <div className="grid gap-4 md:grid-cols-3">
                        <Link href={route('studios.index')} className="rounded-2xl bg-gray-900 p-6 text-white transition hover:bg-gray-800">
                            <p className="text-sm uppercase tracking-[0.2em] text-cyan-300">Studio</p>
                            <h4 className="mt-2 text-xl font-semibold">Lihat daftar studio</h4>
                        </Link>
                        <Link href={route('bookings.index')} className="rounded-2xl bg-cyan-600 p-6 text-white transition hover:bg-cyan-500">
                            <p className="text-sm uppercase tracking-[0.2em] text-cyan-100">Booking</p>
                            <h4 className="mt-2 text-xl font-semibold">Kelola booking saya</h4>
                        </Link>
                        <Link href={route('forum.index')} className="rounded-2xl bg-emerald-600 p-6 text-white transition hover:bg-emerald-500">
                            <p className="text-sm uppercase tracking-[0.2em] text-emerald-100">Forum</p>
                            <h4 className="mt-2 text-xl font-semibold">Masuk forum komunitas</h4>
                        </Link>
                    </div>
                </div>
            </div>
        </AuthenticatedLayout>
    );
}
