#!/usr/bin/env python
import ROOT
import argparse
import re
import subprocess
import sys
import imp
import FWCore.ParameterSet.Config as cms

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)


class Visitor:
    def __init__(self, mode):
        self.mode = mode
        self.file = None

    def enter(self, obj):
        if self.mode == 'all' and self.file is not None and isinstance(obj, cms._Module):
            self.file.write(obj.label() + ' = ' + obj.dumpPython() + '\n')
        if not isinstance(obj, cms.EDFilter):
            return
        if self.mode == 'filters' and self.file is not None and isinstance(obj, cms._Module):
            self.file.write(obj.label() + ' = ' + obj.dumpPython() + '\n')
        label = obj.label()
        name = obj.type_()
        saves = False
        if hasattr(obj, 'saveTags'):
            saves = obj.saveTags.configValue()
        num = None
        if hasattr(obj, 'MinN'):
            num = obj.MinN.configValue()
        if hasattr(obj, 'ncandcut'):
            num = obj.ncandcut.configValue()
        print '    %-40s %-80s %-8s %-6s' % (name, label, saves, num)

    def leave(self, obj):
        pass


def DoFilters(path, menu, save, append=''):
    # print ' '.join(['hltConfigFromDB', '--v2', '--adg', '--configName', menu, '--cff', '--paths', path])
    out = subprocess.check_output(['hltConfigFromDB', '--v2', '--adg' , '--configName', menu, '--cff', '--paths', path])
    module = imp.new_module('trg')
    # for some reason the last line isn't valid config, so I'll remove it
    exec out[:out.rstrip().rfind('\n')] in module.__dict__
    process = cms.Process("MAIN")
    process.extend(module)
    visitor = Visitor(save)
    if save == 'filters':
        visitor.file = open('cfg_filters_%s%s.txt' % (path, append), 'w')
    if save == 'all':
        visitor.file = open('cfg_all_%s%s.txt' % (path, append), 'w')
    print '    %-40s %-80s %-8s %-6s' % ('Type', 'Label', 'Objects', 'Min')
    print '    %s' % ('-'*137)
    getattr(process, path).visit(visitor)
    if visitor.file is not None:
        visitor.file.close()
    return module


parser = argparse.ArgumentParser()


parser.add_argument('--trg', default=None)
parser.add_argument('--map', default=None)
parser.add_argument('--run-range', default=None)
parser.add_argument('--save-cfg', default=None)

args = parser.parse_args()


if args.run_range is not None:
    min_run = int(args.run_range.split(',')[0])
    max_run = int(args.run_range.split(',')[1])

run_menu = {}
run_id = {}

if args.map is not None:
    with open(args.map) as f:
        trg_lines = [line.replace('"', '').split(',') for line in f.read().splitlines() if not line.startswith('#')]
        for line in trg_lines:
            runs = [int(x) for x in line[2:]]
            for r in runs:
                run_menu[r] = line[1]
                run_id[r] = line[0]
# print run_menu

if args.trg is not None:
    with open(args.trg) as f:
        trg_lines = [line.split(',') for line in f.read().splitlines() if not line.startswith('#')]

trg_info = []
for line in trg_lines:
    if len(line) >= 2 and line[1] == 'None':
        continue
    if args.run_range is not None:
        run = int(line[0])
        if run < min_run or run > max_run:
            continue
    trg_info.append(((int(line[0]), int(line[1])), line[2:]))

trg_info.sort(key=lambda x: x[0])

first_run = trg_info[0][0][0]
last_run = trg_info[-1][0][0]

print 'Path %s' % re.match(r'(.*)_v\d+', trg_info[0][1][2].split('/')[0]).group(1)
print ' - first seen in run: %i (%-30s)' % (first_run, run_menu[first_run])
print ' - last seen in run: %-i (%-30s)' % (last_run, run_menu[last_run])

curr_v = None
curr_run = None
curr_menu = None
curr_L1 = None
curr_path = None
curr_L1_set = None

L1_alt_idx = 1
for i, x in enumerate(trg_info):
    # print x
    run = x[0][0]
    path = x[1][2].split('/')[0]
    v = int(re.match(r'.*_v(\d+)', path).group(1))
    menu = run_menu[run]
    L1 = re.sub(r'/\d+', '', x[1][4])
    L1_set = set(L1.split())
    #if path not in L1_per_name:
    #    L1_per_name[path] = L1_set
    #else:
    #    if L1_per_name[path] != L1_set:
    #        print 'Found different L1 seeds for the same trigger version!'
    #        print '>> %s' % path
    #        print '>> %s' % L1_per_name[path]
    #        print '>> %s' % L1_set

    L1 = ' OR '.join(L1.split())
    if curr_v is None:
        print ' - V%i first seen in run %i' % (v, run)
        print '    * HLT menu: %s' % (menu)
        print '    * L1T seed: %s' % (L1)
        print ' - V%i filter sequence:' % (v)
        mod = DoFilters(path, menu, args.save_cfg)
    if curr_v is not None and v != curr_v:
        print ' - V%i last seen in run %i' % (curr_v, curr_run)
        print '    * HLT menu: %s' % (curr_menu)
        print '    * L1T seed: %s' % (curr_L1)
        print ' - V%i first seen in run %i' % (v, run)
        print '    * HLT menu: %s' % (menu)
        print '    * L1T seed: %s' % (L1)
        print ' - V%i filter sequence:' % (v)
        mod = DoFilters(path, menu, args.save_cfg)
        L1_alt_idx = 1
    if i == (len(trg_info) - 1):
        print ' - V%i last seen in run %i' % (v, run)
        print '    * HLT menu: %s' % (menu)
        print '    * L1T seed: %s' % (L1)
    if curr_v is not None and v == curr_v and curr_L1_set != L1_set:
        print ' - V%i has a change in L1 seed in run %i' % (v, run)
        print '    * HLT menu: %s' % (menu)
        print '    * L1T seed: %s' % (L1)
        print ' - V%i filter sequence:' % (v)
        mod = DoFilters(path, menu, args.save_cfg, '_altL1_' + str(L1_alt_idx))
        L1_alt_idx += 1

    curr_v = v
    curr_run = run
    curr_menu = menu
    curr_L1 = L1
    curr_path = path
    curr_L1_set = L1_set

print ('\n\n')


