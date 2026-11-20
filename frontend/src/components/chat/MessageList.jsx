import { BookOpen, UserRound } from "lucide-react";
import ReactMarkdown from "react-markdown";
import SourceCitations from "./SourceCitations";

export default function MessageList({ messages, isLoading = false }) {
    return (
        <div className="mx-auto w-full max-w-3xl space-y-8 px-4 py-8 sm:px-6">
            {messages.map((message) => {
                const isUser = message.role === "user";

                return (
                    <article
                        key={message.id}
                        className={`flex gap-3 sm:gap-4 ${isUser ? "flex-row-reverse" : ""
                            }`}
                    >
                        <div
                            className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${isUser
                                    ? "bg-slate-100 text-slate-600"
                                    : "bg-violet-700 text-white"
                                }`}
                        >
                            {isUser ? (
                                <UserRound size={17} />
                            ) : (
                                <BookOpen size={17} />
                            )}
                        </div>

                        <div
                            className={`min-w-0 max-w-[85%] ${isUser
                                    ? "rounded-2xl rounded-tr-sm bg-white px-5 py-4 shadow-sm ring-1 ring-slate-200"
                                    : "flex-1"
                                }`}
                        >
                            {!isUser && (
                                <p className="mb-2 text-xs font-semibold text-slate-900">
                                    DocuTrace
                                </p>
                            )}

                            {isUser || message.isError ? (
                                <p className="whitespace-pre-wrap break-words text-sm leading-7 text-slate-700">
                                    {message.content}
                                </p>
                            ) : (
                                <div className="min-w-0 break-words text-sm leading-7 text-slate-700">
                                    <ReactMarkdown
                                        components={{
                                            p: ({ children }) => (
                                                <p className="mb-3 last:mb-0">
                                                    {children}
                                                </p>
                                            ),

                                            strong: ({ children }) => (
                                                <strong className="font-semibold text-slate-900">
                                                    {children}
                                                </strong>
                                            ),

                                            ol: ({ children }) => (
                                                <ol className="mb-4 list-decimal space-y-3 pl-5">
                                                    {children}
                                                </ol>
                                            ),

                                            ul: ({ children }) => (
                                                <ul className="mb-4 list-disc space-y-2 pl-5">
                                                    {children}
                                                </ul>
                                            ),

                                            li: ({ children }) => (
                                                <li className="pl-1">
                                                    {children}
                                                </li>
                                            ),

                                            h3: ({ children }) => (
                                                <h3 className="mb-2 mt-5 font-semibold text-slate-900">
                                                    {children}
                                                </h3>
                                            ),

                                            code: ({ children }) => (
                                                <code className="rounded bg-slate-100 px-1.5 py-0.5 font-mono text-xs text-slate-800">
                                                    {children}
                                                </code>
                                            ),

                                            a: ({ href, children }) => (
                                                <a
                                                    href={href}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className="font-medium text-violet-700 underline underline-offset-2 hover:text-violet-900"
                                                >
                                                    {children}
                                                </a>
                                            ),
                                        }}
                                    >
                                        {message.content}
                                    </ReactMarkdown>
                                </div>
                            )}

                            {!isUser && !message.isError && (
                                <SourceCitations
                                    citations={message.citations}
                                />
                            )}
                        </div>
                    </article>
                );
            })}

            {isLoading && (
                <div
                    role="status"
                    aria-live="polite"
                    className="flex items-center gap-3"
                >
                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-violet-700 text-white">
                        <BookOpen size={17} />
                    </div>

                    <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-3">
                        <span className="h-2 w-2 animate-pulse rounded-full bg-violet-400" />
                        <span className="text-xs text-slate-500">
                            Searching company documents...
                        </span>
                    </div>
                </div>
            )}
        </div>
    );
}