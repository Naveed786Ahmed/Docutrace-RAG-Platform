import { useEffect, useMemo, useState } from "react";
import {
    BookOpen,
    Database,
    FileText,
    Search,
    ExternalLink,
    AlertCircle,
    LoaderCircle,
} from "lucide-react";

const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function formatName(value) {
    return value.replaceAll("_", " ").replace(/\.pdf$/i, "");
}

export default function KnowledgeBase() {
    const [data, setData] = useState(null);
    const [search, setSearch] = useState("");
    const [department, setDepartment] = useState("all");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const controller = new AbortController();

        async function loadDocuments() {
            try {
                const response = await fetch(
                    `${API_BASE_URL}/knowledge-base`,
                    { signal: controller.signal }
                );

                if (!response.ok) {
                    throw new Error("Unable to load knowledge base.");
                }

                const result = await response.json();
                setData(result);
            } catch (err) {
                if (err.name !== "AbortError") {
                    setError("Unable to load documents. Please try again.");
                }
            } finally {
                if (!controller.signal.aborted) {
                    setLoading(false);
                }
            }
        }

        loadDocuments();

        return () => controller.abort();
    }, []);

    const documents = useMemo(() => {
        if (!data) return [];

        return data.documents.filter((document) => {
            const matchesSearch = formatName(document.filename)
                .toLowerCase()
                .includes(search.toLowerCase());

            const matchesDepartment =
                department === "all" ||
                document.department === department;

            return matchesSearch && matchesDepartment;
        });
    }, [data, search, department]);

    const stats = [
        {
            label: "Documents",
            value: data?.summary.documents ?? 0,
            icon: FileText,
        },
        {
            label: "Total Pages",
            value: data?.summary.pages ?? 0,
            icon: BookOpen,
        },
        {
            label: "Indexed Chunks",
            value: data?.summary.indexed_chunks ?? 0,
            icon: Database,
        },
    ];

    return (
        <div className="mx-auto w-full max-w-6xl px-5 py-8 sm:px-8 lg:py-10">
            <div className="mb-9">
                <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-violet-700">
                    Document Intelligence
                </p>

                <h1 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
                    Knowledge Base
                </h1>

                <p className="mt-2 text-sm leading-relaxed text-slate-500">
                    Explore the enterprise documents powering your AI assistant.
                </p>
            </div>

            {loading ? (
                <div className="flex items-center gap-3 py-16 text-sm text-slate-500">
                    <LoaderCircle size={19} className="animate-spin" />
                    Loading knowledge base...
                </div>
            ) : error ? (
                <div className="flex items-center gap-3 rounded-xl border border-red-100 bg-red-50 p-5 text-sm text-red-700">
                    <AlertCircle size={19} />
                    {error}
                </div>
            ) : (
                <>
                    <div className="grid gap-4 sm:grid-cols-3">
                        {stats.map(({ label, value, icon: Icon }) => (
                            <div
                                key={label}
                                className="rounded-2xl border border-slate-200 bg-white p-5"
                            >
                                <div className="mb-5 flex h-10 w-10 items-center justify-center rounded-xl bg-violet-50 text-violet-700">
                                    <Icon size={19} />
                                </div>

                                <p className="text-3xl font-semibold tracking-tight text-slate-900">
                                    {value}
                                </p>

                                <p className="mt-1 text-sm text-slate-500">
                                    {label}
                                </p>
                            </div>
                        ))}
                    </div>

                    <div className="mt-10">
                        <div className="mb-5 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
                            <div>
                                <h2 className="text-lg font-semibold text-slate-900">
                                    Document Library
                                </h2>

                                <p className="mt-1 text-sm text-slate-500">
                                    {documents.length} documents available
                                </p>
                            </div>

                            <div className="flex flex-col gap-3 sm:flex-row">
                                <div className="relative">
                                    <Search
                                        size={17}
                                        className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                                    />

                                    <input
                                        type="search"
                                        value={search}
                                        onChange={(event) => setSearch(event.target.value)}
                                        placeholder="Search documents..."
                                        aria-label="Search documents"
                                        className="w-full rounded-xl border border-slate-200 bg-white py-2.5 pl-10 pr-4 text-sm text-slate-800 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-100 sm:w-60"
                                    />
                                </div>

                                <select
                                    value={department}
                                    onChange={(event) => setDepartment(event.target.value)}
                                    aria-label="Filter by department"
                                    className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-700 outline-none focus:border-violet-400"
                                >
                                    <option value="all">All departments</option>

                                    {Object.keys(data.departments).map((name) => (
                                        <option key={name} value={name}>
                                            {formatName(name)}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
                            {documents.length === 0 ? (
                                <div className="px-6 py-14 text-center">
                                    <FileText
                                        size={25}
                                        className="mx-auto mb-3 text-slate-300"
                                    />

                                    <p className="text-sm font-medium text-slate-700">
                                        No matching documents
                                    </p>

                                    <p className="mt-1 text-xs text-slate-400">
                                        Try a different search or department.
                                    </p>
                                </div>
                            ) : (
                                <div className="divide-y divide-slate-100">
                                    {documents.map((document) => (
                                        <div
                                            key={`${document.department}/${document.filename}`}
                                            className="flex flex-col gap-4 px-5 py-4 transition hover:bg-slate-50/70 sm:flex-row sm:items-center sm:justify-between"
                                        >
                                            <div className="flex min-w-0 items-start gap-3">
                                                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-600">
                                                    <FileText size={20} />
                                                </div>

                                                <div className="min-w-0">
                                                    <p className="break-words text-sm font-semibold text-slate-900">
                                                        {formatName(document.filename)}
                                                    </p>

                                                    <p className="mt-1 text-xs text-slate-500">
                                                        {formatName(document.department)}
                                                        {" · "}
                                                        {document.pages} pages
                                                        {" · "}
                                                        PDF
                                                    </p>
                                                </div>
                                            </div>

                                            <a
                                                href={`${API_BASE_URL}${document.url}`}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="inline-flex shrink-0 items-center justify-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-700 transition hover:border-violet-200 hover:bg-violet-50 hover:text-violet-700"
                                            >
                                                View document
                                                <ExternalLink size={14} />
                                            </a>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}