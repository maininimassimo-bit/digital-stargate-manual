<?php
// Only the local, authenticated WebUI may access the manual review gate.
require_once __DIR__ . '/includes/functions.php';
initialize_variables();
$csrf_token = useLogin();
header('Cache-Control: no-store, private');
header('X-Robots-Tag: noindex, nofollow');
header('X-Content-Type-Options: nosniff');
header("Content-Security-Policy: default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'self'; base-uri 'none'");
if (!$useLogin || !is_logged_in()) {
    http_response_code(403);
    echo 'Accedi prima all’amministrazione Allsky. <a href="/index.php">Apri amministrazione</a>';
    exit;
}
function h($text) { return htmlspecialchars((string) $text, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
function review_call($request) {
    $socket = @stream_socket_client('unix:///run/dsg-meteor-review/review.sock', $errno, $error, 3);
    if (!$socket) throw new RuntimeException('Servizio di revisione non disponibile.');
    stream_set_timeout($socket, 10);
    $payload = json_encode($request) . "\n";
    if (fwrite($socket, $payload) !== strlen($payload)) { fclose($socket); throw new RuntimeException('Richiesta non inviata.'); }
    $raw = fgets($socket, 3000000);
    fclose($socket);
    $response = json_decode($raw ?: '', true);
    if (!is_array($response) || empty($response['ok'])) throw new RuntimeException($response['error'] ?? 'Risposta non valida.');
    return $response['result'];
}
$message = ''; $errorMessage = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!CSRFValidate()) { http_response_code(403); exit('Richiesta rifiutata: aggiorna la pagina.'); }
    $action = $_POST['action'] ?? '';
    if (!in_array($action, ['approve', 'reject'], true) || ($action === 'approve' && ($_POST['reviewed'] ?? '') !== 'yes')) {
        http_response_code(400); exit('Conferma la revisione prima di pubblicare.');
    }
    try {
        $result = review_call(['action' => $action, 'stamp' => $_POST['stamp'] ?? '', 'version' => $_POST['version'] ?? '', 'actor' => (string) ($_SESSION['user'] ?? 'WebUI-admin')]);
        $_SESSION['meteor_review_message'] = $action === 'approve' ? 'Candidato approvato per la galleria pubblica. Rimane un candidato da verificare scientificamente.' : 'Candidato escluso dalla pubblicazione. L’originale privato è conservato.';
        header('Location: /meteor-review.php', true, 303); exit;
    } catch (RuntimeException $exc) { $errorMessage = $exc->getMessage(); }
}
$message = $_SESSION['meteor_review_message'] ?? ''; unset($_SESSION['meteor_review_message']);
$queue = ['pending' => [], 'cutoff' => '']; $preview = null; $stamp = $_GET['stamp'] ?? '';
try {
    $queue = review_call(['action' => 'list']);
    if ($stamp !== '') $preview = review_call(['action' => 'preview', 'stamp' => $stamp]);
} catch (RuntimeException $exc) { $errorMessage = $exc->getMessage(); }
?>
<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Revisione meteore · Digital Stargate</title>
<style>body{background:#081521;color:#dce8f1;font:16px system-ui;margin:0 auto;padding:24px;max-width:1100px}a{color:#60d9ed}section{border:1px solid #28546a;border-radius:12px;padding:18px;margin:20px 0}img{max-width:100%;height:auto}button{padding:12px;margin:12px 12px 0 0;cursor:pointer}label{display:block;margin:16px 0}.error{color:#ffb0a5}.success{color:#8fedbd}li{margin:12px 0}</style></head><body>
<a href="/index.php?page=list_meteors&amp;day=All">← Amministrazione Allsky</a><h1>Revisione dei nuovi candidati temporali</h1>
<p>Pubblicazione esclusivamente dopo revisione manuale. Lo storico privato è escluso. Il rilevatore attuale resta attivo.</p>
<p>Inizio dei nuovi candidati: <strong><?=h($queue['cutoff'])?></strong> (UTC). Le approvazioni non certificano l’origine meteorica.</p>
<?php if ($message): ?><p class="success"><?=h($message)?></p><?php endif ?>
<?php if ($errorMessage): ?><p class="error"><?=h($errorMessage)?></p><?php endif ?>
<?php if ($preview): ?><section><h2>Fotogramma <?=h($stamp)?></h2><p><?=h($preview['traces'])?> tracce automatiche. I cerchi indicano gli estremi delle tracce e compaiono soltanto nell’anteprima privata.</p>
<img alt="Anteprima privata del candidato" src="data:image/jpeg;base64,<?=h($preview['image'])?>">
<form method="post" action="/meteor-review.php"><input type="hidden" name="csrf_token" value="<?=h($csrf_token)?>"><input type="hidden" name="stamp" value="<?=h($stamp)?>"><input type="hidden" name="version" value="<?=h($preview['version'])?>">
<label><input type="checkbox" name="reviewed" value="yes"> Ho esaminato la traccia ed escludo evidenti aerei, satelliti, nuvole o riflessi; autorizzo la pubblicazione di questo candidato.</label>
<button name="action" value="approve">Pubblica candidato esaminato</button><button name="action" value="reject">Escludi dalla pubblicazione</button></form></section><?php endif ?>
<section><h2>In attesa di revisione: <?=count($queue['pending'])?></h2><?php if (!$queue['pending']): ?><p>Nessun nuovo candidato da esaminare.</p><?php else: ?><ul><?php foreach ($queue['pending'] as $candidate): ?><li><a href="?stamp=<?=h($candidate['stamp'])?>"><?=h($candidate['stamp'])?></a> · <?=h($candidate['traces'])?> tracce</li><?php endforeach ?></ul><?php endif ?></section>
<p>Le immagini pubbliche già presenti non vengono sovrascritte. Esclusione e approvazione sono registrate privatamente.</p></body></html>
