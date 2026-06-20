import PublicLayout from '@/Layouts/PublicLayout';
import { Head, Link, usePage } from '@inertiajs/react';

export default function Index({ studios }) {
    const flash = usePage().props.flash;

    return (
        <PublicLayout title="Studios">
            <Head title="Studios" />

            {flash.success && (
                <div className="mb-6 rounded-xl border border-emerald-400/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
                    {flash.success}
                </div>
            )}

            {flash.error && (
                <div className="mb-6 rounded-xl border border-rose-400/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
                    {flash.error}
                </div>
            )}

            {studios.length === 0 ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 p-8 text-center">
                    <p className="text-sm text-white/70">Belum ada studio tersedia saat ini.</p>
                </div>
            ) : (
                <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
                    {studios.map((studio) => (
                    <article key={studio.id} className="rounded-2xl border border-white/10 bg-white/5 p-5 shadow-2xl shadow-black/20">
                        <div className="flex items-start justify-between gap-4">
                            <div>
                                <p className="text-xs uppercase tracking-[0.25em] text-cyan-300">{studio.type}</p>
                                <h2 className="mt-2 text-xl font-semibold text-white">{studio.name}</h2>
                            </div>
                            <div className="rounded-full bg-cyan-400/15 px-3 py-1 text-sm font-medium text-cyan-200">
                                Rp {studio.price_per_hour} / jam
                            </div>
                        </div>

                        <p className="mt-4 line-clamp-3 text-sm leading-6 text-white/70">{studio.description}</p>
                        <p className="mt-4 text-sm text-white/60">{studio.location}</p>
                        <p className="mt-2 text-sm text-white/60">{studio.schedules.length} jadwal tersedia</p>

                        <Link
                            href={route('studios.show', studio.slug)}
                            className="mt-5 inline-flex items-center rounded-full bg-white px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300"
                        >
                            Lihat detail
                        </Link>
                    </article>
                    ))}
                </div>
            )}
        </PublicLayout>
    );
}