'use client'

import { useState } from 'react'
import Sidebar from '@/components/Sidebar'
import Editor from '@/components/Editor'

export default function Home() {
  const [content, setContent] = useState('<p>씬을 작성하세요...</p>')

  return (
    <div className="flex h-screen">
      <Sidebar />
      
      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b border-gray-200 p-4">
          <h1 className="text-lg font-semibold">씬 1: 냉동실</h1>
          <p className="text-sm text-gray-600">1장. 깨어남</p>
        </header>

        <main className="flex-1 overflow-auto bg-gray-50 p-8">
          <div className="max-w-4xl mx-auto">
            <Editor
              content={content}
              onChange={setContent}
              placeholder="씬을 작성하세요..."
            />
          </div>
        </main>

        <footer className="bg-white border-t border-gray-200 p-4 flex justify-between items-center">
          <div className="text-sm text-gray-600">
            자동 저장됨 • 단어 수: {content.replace(/<[^>]*>/g, '').split(/\s+/).length}
          </div>
          <div className="flex gap-2">
            <button className="px-4 py-2 text-sm bg-gray-200 rounded hover:bg-gray-300">
              버전 기록
            </button>
            <button className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700">
              저장
            </button>
          </div>
        </footer>
      </div>
    </div>
  )
}
        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            To get started, edit the page.tsx file.
          </h1>
          <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            Looking for a starting point or more instructions? Head over to{" "}
            <a
              href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
              className="font-medium text-zinc-950 dark:text-zinc-50"
            >
              Templates
            </a>{" "}
            or the{" "}
            <a
              href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
              className="font-medium text-zinc-950 dark:text-zinc-50"
            >
              Learning
            </a>{" "}
            center.
          </p>
        </div>
        <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
          <a
            className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
            href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={16}
              height={16}
            />
            Deploy Now
          </a>
          <a
            className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-black/[.08] px-5 transition-colors hover:border-transparent hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] md:w-[158px]"
            href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            Documentation
          </a>
        </div>
      </main>
    </div>
  );
}
