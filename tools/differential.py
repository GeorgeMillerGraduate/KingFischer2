#!/usr/bin/env python3
"""Reproducible move-generation + NNUE oracle checks. Requires python-chess and a reference Stockfish.
The reference is development-only; JengaFish runtime never imports or launches it.
"""
import argparse,json,random,re,subprocess,time,pathlib
import chess

def launch(command):
    return subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
def send(p,line):
    p.stdin.write(line+'\n');p.stdin.flush()
def until(p,marker):
    lines=[]
    while True:
        line=p.stdout.readline()
        if not line: raise RuntimeError('Engine exited: '+p.stderr.read())
        line=line.strip();lines.append(line)
        if marker(line):return lines

def corpus(count):
    rng=random.Random(20260911);b=chess.Board();result=[]
    while len(result)<count:
        if b.is_game_over() or b.fullmove_number>130:b=chess.Board()
        result.append(b.fen(en_passant='fen'))
        b.push(rng.choice(list(b.legal_moves)))
    return result

def main():
    a=argparse.ArgumentParser();a.add_argument('--stockfish',required=True);a.add_argument('--jar',default='JengaFish.jar');a.add_argument('--positions',type=int,default=1000);a.add_argument('--output',default='docs/differential-results.json');args=a.parse_args()
    sf=launch([args.stockfish]);jf=launch(['java','-Xmx768m','-jar',args.jar]);positions=corpus(args.positions)
    counts={'positions':len(positions),'legal_move_sets':0,'perft_depth_2':0,'nnue_raw':0,'normalized_eval':0};start=time.monotonic()
    try:
        for index,fen in enumerate(positions):
            b=chess.Board(fen)
            for p in (sf,jf):send(p,'position fen '+fen);send(p,'go perft 2')
            refs=[]
            for p in (sf,jf):
                lines=until(p,lambda s:s.startswith('Nodes searched:'))
                moves={s.split(':')[0]:int(s.split(':')[1]) for s in lines if re.match(r'^[a-h][1-8][a-h][1-8][qrbn]?: \d+$',s)}
                refs.append((moves,int(lines[-1].split(':')[1])))
            assert refs[0]==refs[1],('perft mismatch',index,fen,refs)
            assert set(refs[0][0])=={m.uci() for m in b.legal_moves},('legal moves mismatch',fen)
            counts['legal_move_sets']+=1;counts['perft_depth_2']+=1
            if not b.is_check():
                for p in (sf,jf):send(p,'eval');send(p,'isready')
                s='\n'.join(until(sf,lambda s:s=='readyok'));j='\n'.join(until(jf,lambda s:s=='readyok'))
                
                if not re.search(r'NNUE evaluation\s+([+-]?\d+) \(side to move, internal units\)',s): raise RuntimeError((index,fen,s,j))
                sr=int(re.search(r'NNUE evaluation\s+([+-]?\d+) \(side to move, internal units\)',s)[1]);jr=int(re.search(r' raw (-?\d+)',j)[1])
                assert sr==jr,('NNUE mismatch',index,fen,sr,jr,s,j)
                sfcp=round(float(re.search(r'Final evaluation\s+([+-]?\d+\.\d+)',s)[1])*100)*(1 if b.turn else -1)
                jcp=int(re.search(r' cp (-?\d+)',j)[1]);assert sfcp==jcp,('eval cp mismatch',index,fen,sfcp,jcp)
                counts['nnue_raw']+=1;counts['normalized_eval']+=1
            if (index+1)%100==0:print('Validated',index+1,flush=True)
    finally:
        for p in (sf,jf):
            if p.poll() is None:send(p,'quit');p.wait(timeout=10)
    counts['elapsed_seconds']=round(time.monotonic()-start,2);counts['seed']=20260911;counts['reference_commit']='59aae690f91d6f69aac194f447d84b4a2c3be778'
    pathlib.Path(args.output).write_text(json.dumps(counts,indent=2)+'\n')
    pathlib.Path(args.output).with_suffix('.fens').write_text('\n'.join(positions)+'\n')
    print(json.dumps(counts,indent=2))
if __name__=='__main__':main()
