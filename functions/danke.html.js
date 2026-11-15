// Cloudflare Pages Function: nimmt das Formular «sichtbarkeits-check» an
// und reicht es im gleichen Format wie Netlify Forms an die Make-Automation weiter.
// Webhook-Adresse liegt als Geheimnis MAKE_WEBHOOK_URL in Cloudflare (nicht im Code).
export async function onRequestPost({ request, env }) {
  const back = (path) => Response.redirect(new URL(path, request.url).toString(), 303);
  let fd;
  try { fd = await request.formData(); } catch (e) { return back('/sichtbarkeits-check'); }

  // Spam-Falle: echtes Formular lässt dieses Feld leer
  if (String(fd.get('firma-website') || '').trim()) return back('/danke');

  const data = {};
  for (const [k, v] of fd.entries()) {
    if (typeof v !== 'string' || k === 'firma-website' || k === 'form-name') continue;
    data[k] = v.trim();
  }
  if (!data.email) return back('/sichtbarkeits-check');

  const payload = {
    form_name: 'sichtbarkeits-check',
    site_url: new URL(request.url).origin,
    created_at: new Date().toISOString(),
    name: data.name || '',
    email: data.email,
    data,
  };
  const r = await fetch(env.MAKE_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!r.ok) {
    return new Response('Die Anfrage konnte gerade nicht gesendet werden. Bitte rufen Sie an: +41 76 339 13 98', { status: 502, headers: { 'content-type': 'text/plain; charset=utf-8' } });
  }
  return back('/danke');
}
