import { useEffect, useRef, useState } from "react";

import Sidebar from "./components/layout/Sidebar";
import Header from "./components/layout/Header";
import WelcomeScreen from "./components/chat/WelcomeScreen";
import ChatInput from "./components/chat/ChatInput";
import MessageList from "./components/chat/MessageList";
import { sendChatMessage } from "./services/api";
import KnowledgeBase from "./components/knowledge/KnowledgeBase";

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activePage, setActivePage] = useState("chat");

  const controllerRef = useRef(null);
  const conversationRef = useRef(0);

  useEffect(() => {
    return () => controllerRef.current?.abort();
  }, []);

  async function handleSend(question) {
    if (isLoading || !question.trim()) return;

    const conversationId = conversationRef.current;

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };

    setMessages((previous) => [...previous, userMessage]);
    setIsLoading(true);

    const controller = new AbortController();
    controllerRef.current = controller;

    try {
      const result = await sendChatMessage(
        question,
        controller.signal
      );

      if (conversationRef.current !== conversationId) return;

      const assistantMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: result.answer,
        citations: result.citations ?? [],
      };

      setMessages((previous) => [...previous, assistantMessage]);
    } catch (error) {
      if (
        error.name === "AbortError" ||
        conversationRef.current !== conversationId
      ) {
        return;
      }

      setMessages((previous) => [
        ...previous,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "Unable to process your request. Please try again.",
          citations: [],
          isError: true,
        },
      ]);
    } finally {
      if (conversationRef.current === conversationId) {
        setIsLoading(false);
        controllerRef.current = null;
      }
    }
  }

  function handleNewConversation() {
    conversationRef.current += 1;
    controllerRef.current?.abort();
    controllerRef.current = null;

    setMessages([]);
    setIsLoading(false);
    setSidebarOpen(false);
    setActivePage("chat");
  }

  function handleNavigate(page) {
    setActivePage(page);
    setSidebarOpen(false);
  }

  return (
    <div className="flex h-dvh overflow-hidden bg-[#FAFAFC]">
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onNewConversation={handleNewConversation}
        activePage={activePage}
        onNavigate={handleNavigate}
      />

      <main className="flex min-w-0 flex-1 flex-col">
        <Header
          onMenuClick={() => setSidebarOpen(true)}
          activePage={activePage}
        />

        <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {activePage === "knowledge" ? (
            <KnowledgeBase />
          ) : messages.length === 0 ? (
            <WelcomeScreen onSuggestionClick={handleSend} />
          ) : (
            <MessageList
              messages={messages}
              isLoading={isLoading}
            />
          )}
        </div>

        {activePage === "chat" && (
          <div className="shrink-0 border-t border-slate-100 bg-[#FAFAFC] px-4 py-4 sm:px-6">
            <div className="mx-auto w-full max-w-3xl">
              <ChatInput
                onSend={handleSend}
                disabled={isLoading}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}