import InputError from '@/Components/InputError';
import PrimaryButton from '@/Components/PrimaryButton';
import TextInput from '@/Components/TextInput';
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import { Head, useForm, usePage } from '@inertiajs/react';

function CommentForm({ postId }) {
    const { data, setData, post, processing, errors, reset } = useForm({
        forum_post_id: postId,
        content: '',
    });

    const submit = (event) => {
        event.preventDefault();

        post(route('forum.comments.store'), {
            preserveScroll: true,
            onSuccess: () => reset('content'),
        });
    };

    return (
        <form onSubmit={submit} className="mt-4 space-y-2">
            <textarea
                className="block w-full rounded-lg border-gray-200 text-sm shadow-sm focus:border-gray-400 focus:ring-gray-400"
                rows="3"
                value={data.content}
                onChange={(event) => setData('content', event.target.value)}
                placeholder="Tulis komentar..."
            />
            <InputError message={errors.content} />
            <PrimaryButton disabled={processing}>Kirim komentar</PrimaryButton>
        </form>
    );
}

export default function Index({ posts }) {
    const flash = usePage().props.flash;
    const { data, setData, post, processing, errors, reset } = useForm({
        title: '',
        content: '',
    });

    const submit = (event) => {
        event.preventDefault();

        post(route('forum.posts.store'), {
            preserveScroll: true,
            onSuccess: () => reset(),
        });
    };

    return (
        <AuthenticatedLayout
            header={<h2 className="text-xl font-semibold leading-tight text-gray-800">Forum Komunitas</h2>}
        >
            <Head title="Forum" />

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

                    <section className="rounded-2xl bg-white p-6 shadow-sm">
                        <h3 className="text-lg font-semibold text-gray-900">Buat postingan baru</h3>
                        <form onSubmit={submit} className="mt-4 space-y-4">
                            <div>
                                <TextInput
                                    type="text"
                                    className="block w-full"
                                    value={data.title}
                                    onChange={(event) => setData('title', event.target.value)}
                                    placeholder="Judul postingan"
                                />
                                <InputError message={errors.title} className="mt-2" />
                            </div>

                            <div>
                                <textarea
                                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                    rows="4"
                                    value={data.content}
                                    onChange={(event) => setData('content', event.target.value)}
                                    placeholder="Ceritakan diskusi musikmu..."
                                />
                                <InputError message={errors.content} className="mt-2" />
                            </div>

                            <PrimaryButton disabled={processing}>{processing ? 'Mengirim...' : 'Post'}</PrimaryButton>
                        </form>
                    </section>

                    {posts.length === 0 ? (
                        <div className="rounded-2xl bg-white p-8 shadow-sm">
                            <p className="text-sm text-gray-600">Belum ada postingan forum. Jadilah yang pertama memulai diskusi.</p>
                        </div>
                    ) : (
                        <div className="grid gap-4">
                            {posts.map((postItem) => (
                            <article key={postItem.id} className="rounded-2xl bg-white p-6 shadow-sm">
                                <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                                    <div>
                                        <h3 className="text-lg font-semibold text-gray-900">{postItem.title}</h3>
                                        <p className="text-sm text-gray-500">oleh {postItem.user.name}</p>
                                    </div>
                                    <span className="text-xs uppercase tracking-wide text-gray-400">{postItem.created_at}</span>
                                </div>
                                <p className="mt-4 whitespace-pre-line text-gray-700">{postItem.content}</p>

                                <div className="mt-6 border-t border-gray-100 pt-4">
                                    <h4 className="text-sm font-semibold text-gray-900">Komentar</h4>
                                    <div className="mt-3 space-y-3">
                                        {postItem.comments.map((comment) => (
                                            <div key={comment.id} className="rounded-xl bg-gray-50 p-3">
                                                <p className="text-sm font-medium text-gray-900">{comment.user.name}</p>
                                                <p className="text-sm text-gray-700">{comment.content}</p>
                                            </div>
                                        ))}
                                        {postItem.comments.length === 0 && (
                                            <p className="text-sm text-gray-500">Belum ada komentar.</p>
                                        )}
                                    </div>

                                    <CommentForm postId={postItem.id} />
                                </div>
                            </article>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </AuthenticatedLayout>
    );
}