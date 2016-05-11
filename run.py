#!/usr/bin/env python3
from dolphin import runDolphin
from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("--name", type=str,
                    help="filename to import from and save to")

parser.add_argument("--tag", type=str,
                    help="optional tag to mark experiences")

parser.add_argument("--nodump", dest='dump', action="store_false",
                    help="don't dump experiences to disk")

parser.add_argument("--dump_max", type=int,
                   help="caps number of experiences")

parser.add_argument("--dolphin_dir", type=str,
                   help="dolphin user directory")

parser.add_argument("--parallel", type=int, help="spawn parallel cpus")

parser.add_argument("--dolphin", action="store_true", help="run dolphin")
parser.add_argument("--movie", type=str, help="movie to play on dolphin startup")
args = parser.parse_args()

def runCPU(args):
  from cpu import CPU
  CPU(**args).run()

if args.parallel is None:
  runCPU(args.__dict__)
else:
  from multiprocessing import Process
  processes = []
  for i in range(args.parallel):
    d = args.__dict__.copy()
    d['tag'] = i
    user = 'parallel/%d/' % i
    d['dolphin_dir'] = user
    runner = Process(target=runCPU, args=[d])
    runner.start()

    dolphin = runDolphin(user=user, count=args.parallel, movie=args.movie)
    processes.append((runner, dolphin))

  try:
    for r, d in processes:
      r.join()
      d.wait()
  except KeyboardInterrupt:
    for p, d in processes:
      p.terminate()
      d.terminate()
