(() => {
  'use strict';

  const normalizeId = (value) => String(value || '').trim();
  const sortKey = (session) => `${String(session?.observationDate || '')}\u0000${normalizeId(session?.sessionId)}`;

  const latestSession = (sessions) => [...(Array.isArray(sessions) ? sessions : [])]
    .filter((session) => normalizeId(session?.sessionId))
    .sort((left, right) => sortKey(right).localeCompare(sortKey(left)))[0] || null;

  const resolve = (requestedSessionId, sessions) => {
    const requested = normalizeId(requestedSessionId);
    if (requested) return Object.freeze({ sessionId: requested, source: 'requested' });
    const latest = latestSession(sessions);
    return latest
      ? Object.freeze({ sessionId: normalizeId(latest.sessionId), source: 'latest' })
      : null;
  };

  const withSessionId = (href, sessionId) => {
    const url = new URL(href);
    url.searchParams.set('sessionId', normalizeId(sessionId));
    return url.href;
  };

  window.DSGScientificSessionDetailRouting = Object.freeze({ latestSession, resolve, withSessionId });
})();
