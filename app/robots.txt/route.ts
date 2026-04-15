import { NextResponse } from 'next/server'

export function GET(request: Request) {
  const origin = new URL(request.url).origin
  const txt = `User-agent: *\nAllow: /\nSitemap: ${origin}/sitemap.xml\n`
  return new Response(txt, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  })
}
