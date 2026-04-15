export function GET(request: Request) {
  const origin = new URL(request.url).origin
  const pages = [
    '/',
    '/browse',
    '/about',
    '/ethiopian',
    '/dashboard',
    '/login',
    '/register',
    '/credits'
  ]
  const lastmod = new Date().toISOString()
  const urls = pages.map((p) => {
    return `  <url>\n    <loc>${origin}${p}</loc>\n    <lastmod>${lastmod}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>`
  }).join('\n')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>`

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' }
  })
}
