import os
import time

import dask
from coffea import hist
from coffea import processor as processor
from coffea.analysis_objects import JaggedCandidateArray
from coffea.processor.test_items import NanoTestProcessor, NanoEventsProcessor
from coffea.util import save
from dask.distributed import Client

from coffea_casa import CoffeaCasaCluster

filelist = {
    "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8": [
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/16B6B7CD-4310-A042-AB52-7DA8ADA22922.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/05884C27-75AD-D340-B515-7017F9655675.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/0CA4B9C4-805D-C148-8281-D615F9DE8541.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/12C1D5AD-DFFB-F547-A634-17FE8AAB84B1.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/0F49C966-5F44-3D4F-AADF-F820A2EBF8A9.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/1A9BA6F1-F51D-F342-BB5D-F0F3B17ED70E.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/168D358A-B3B2-6849-9EF4-D2B6791A26AA.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/26884FA0-B96A-1745-AA11-597C5168EF5E.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/1C3AC8F7-987B-4D40-B002-767A2C65835B.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/FC56B1DA-20B9-F14A-A2CF-2097B8095BEB.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/AF265BB7-CF6C-8241-8DC2-F13BA8A9AD60.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/AF34E3F0-25B7-6644-B557-1428CF675FDC.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/A5702444-A58D-364F-BF6C-EF28C9C52344.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/AB329578-42CC-4746-A15D-08E70CD2554E.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/9F70ACE0-A9C2-494C-B0E5-42E7017ABF95.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/A1B3E169-6D65-E44E-B891-8F738CBB78AD.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/932CE866-A30E-F34D-B0D5-4C4CEAA06CB8.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/948182F2-9993-C74D-B2EA-1D6E0098AD61.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/8F3EEF08-F61E-4046-B140-B04B87602708.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/8FA629F5-385A-AD4A-BB6F-D0856E633712.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/2A9A7EDE-2249-2C44-AF6D-E44B83E8CBDF.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/3C0F69F9-2D31-6646-A1B0-FE021BE707C8.root",
        "root://xcache//store/mc/RunIIAutumn18NanoAODv5/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/110000/274599AC-1636-3641-B09F-ECA42B8F63A4.root",
    ],
}

# Wrapper aroung dask_queue.HTCondorCluster, that allowed to launch Dask on an HTCondor cluster with a shared file system and customised for our analysis facility.
# More information: https://jobqueue.dask.org/en/latest/generated/dask_jobqueue.HTCondorCluster.html
cluster = CoffeaCasaCluster()
cluster.scale(10)
client = Client(cluster)

# A lot of interesting configuration:
# * client (distributed.client.Client) – A dask distributed client instance
# * savemetrics': (int, optional) -  save metrics for I/O analysis
# * compression (int, optional) – Compress accumulator outputs in flight with LZ4, at level specified (default 1). Set to None for no compression.
# * priority (int, optional) – Task priority, default 0
# * nano, mmap, flatten, cache_strategy, xrootdsettings and many more....
config = {
    'client': client,
    'compression': 1,
    'savemetrics': 1,
    # 'xrootdconfig': {
    #     'chunkbytes': 1024*128,
    #     'limitbytes': 200 * 1024**2
    # },
    #'cachestrategy': 'dask-worker',
    #'worker_affinity': True,
    'nano': True,
    #'priority': 1,
}

# Maximum number of chunks to process per dataset
chunksize = 100000

# We are using a piece only: 17 Gb piece of dataset only
p = NanoEventsProcessor(canaries=['0001fd0d874c9fff11e9a13cd2e55d9fbeef;Events;0;99159;Muon_pt'])

# A convenience wrapper to submit jobs for a file set, which is a dictionary of dataset: [file list] entries.
# Supports only uproot reading, via the LazyDataFrame class.
# * Parameters: processor_instance (ProcessorABC) – An instance of a class deriving from ProcessorABC
# * Parameters: executor (callable) – A function that takes 3 arguments: items, function, accumulator and performs some action equivalent to: `for item in items: accumulator += function(item)`. See iterative_executor, futures_executor, dask_executor, or parsl_executor for available options.
# * Parameters: executor_args (dict, optional) – Arguments to pass to executor.
# * Parameters: pre_args (dict, optional) – Similar to executor_args, defaults to executor_args
# * Parameters: chunksize (int, optional) – Maximum number of entries to process at a time in the data frame
# * Parameters: maxchunks (int, optional) – Maximum number of chunks to process per dataset Defaults to processing the whole dataset
tic = time.time()
res = processor.run_uproot_job(filelist, 'Events', p, processor.dask_executor, config, chunksize=chunksize, maxchunks=None, pre_args={'client': client})
toc = time.time()

# Let's print some staistics:
print("Dask client:", client)
print("Total time: %.0f" % (toc - tic))
print("Events / s / thread: {:,.0f}".format(res[1]['entries'].value / res[1]['processtime'].value))
print("Bytes / s / thread: {:,.0f}".format(res[1]['bytesread'].value / res[1]['processtime'].value))
print("Events / s: {:,.0f}".format(res[1]['entries'].value / (toc - tic)))
print("Bytes / s: {:,.0f}".format(res[1]['bytesread'].value / (toc - tic)))
