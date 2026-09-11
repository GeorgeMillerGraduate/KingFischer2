#!/usr/bin/env python3
"""Exercise the executable's asynchronous UCI lifecycle and validate every reported PV."""
import argparse,subprocess,threading,queue,time,re,json,pathlib
import chess
p=argparse.ArgumentParser();p.add_argument('--jar',default='JengaFish.jar');p.add_argument('--output',default='docs/uci-results.json');a=p.parse_args()
proc=subprocess.Popen(['java','-Xmx768m','-jar',a.jar],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
q=queue.Queue()
def reader():
    for line in proc.stdout:q.put(line.strip())
threading.Thread(target=reader,daemon=True).start()
results={};board=chess.Board()
def send(s):proc.stdin.write(s+'\n');proc.stdin.flush()
def until(marker,timeout=20):
    lines=[];end=time.monotonic()+timeout
    while True:
        line=q.get(timeout=max(.001,end-time.monotonic()));lines.append(line)
        if line.startswith('info depth ') and ' pv ' in line:
            b=board.copy()
            for text in line.split(' pv ',1)[1].split():
                m=chess.Move.from_uci(text);assert m in b.legal_moves,('illegal PV',line,b.fen());b.push(m)
        if marker(line):return lines

def best(timeout=20):
    lines=until(lambda s:s.startswith('bestmove '),timeout);move=lines[-1].split()[1]
    assert move=='0000' or chess.Move.from_uci(move) in board.legal_moves
    if ' ponder ' in lines[-1]:
        b=board.copy();b.push_uci(move);assert chess.Move.from_uci(lines[-1].split(' ponder ')[1]) in b.legal_moves
    return lines
try:
    send('uci');lines=until(lambda s:s=='uciok');assert any(s.startswith('id name JengaFish') for s in lines);results['handshake']='passed'
    send('isready');until(lambda s:s=='readyok')
    send('eval');send('isready');until(lambda s:s=='readyok')
    send('go infinite');until(lambda s:s.startswith('info depth '))
    start=time.monotonic();send('isready');until(lambda s:s=='readyok',2);results['ready_during_search_ms']=round((time.monotonic()-start)*1000)
    start=time.monotonic();send('stop');best(2);results['stop_response_ms']=round((time.monotonic()-start)*1000)
    send('setoption name Clear Hash');send('go depth 7');lines=best(60);assert any(s.startswith('info depth 7 ') for s in lines);results['depth_7_legal_pvs']='passed'
    send('setoption name MultiPV value 3');send('go depth 3');lines=best();final=[s for s in lines if s.startswith('info depth 3 ')];assert len(final)==3;assert len({s.split(' pv ')[1].split()[0] for s in final})==3;results['multipv']='passed'
    send('setoption name MultiPV value 1');send('go depth 3 searchmoves e2e4');assert best()[-1].split()[1]=='e2e4';results['searchmoves']='passed'
    send('go nodes 1');best();results['tiny_node_limit']='passed'
    start=time.monotonic();send('go movetime 150');best(3);duration=round((time.monotonic()-start)*1000);assert duration<1500;results['movetime_150_actual_ms']=duration
    send('go ponder depth 2');until(lambda s:s.startswith('info depth 2 '));send('isready');lines=until(lambda s:s=='readyok');assert not any(s.startswith('bestmove') for s in lines);send('ponderhit');best(2);results['ponderhit']='passed'
    send('go infinite depth 1');until(lambda s:s.startswith('info depth 1 '));send('isready');lines=until(lambda s:s=='readyok');assert not any(s.startswith('bestmove') for s in lines);send('stop');best(2);results['infinite_waits_for_stop']='passed'
    send('position startpos moves e2e4 e7e5 g1f3');board.push_uci('e2e4');board.push_uci('e7e5');board.push_uci('g1f3');send('go depth 4');best();results['position_moves']='passed'
    send('position startpos moves e2e5');send('setoption name Hash value nope');send('setoption name UCI_Chess960 value true');send('go depth');send('isready');lines=until(lambda s:s=='readyok');assert len([s for s in lines if s.startswith('info string Error:')])==4;send('go depth 3');best();results['malformed_input_recovery']='passed'
    send('go infinite');until(lambda s:s.startswith('info depth '));send('quit');proc.wait(timeout=3);assert proc.returncode==0;results['quit_during_search']='passed'
finally:
    if proc.poll() is None:proc.kill();proc.wait()
pathlib.Path(a.output).write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
