"use client";

import TranslationManagement from "@/components/TranslationManagement";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-stone-100 dark:bg-stone-900 text-stone-800 dark:text-stone-200 font-[family-name:var(--font-geist-sans)]">
      <Header />
      <TranslationManagement />
      <Footer />
    </div>
  );
}
