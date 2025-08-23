"""
Linear Drift Compensation
Currently implements drift correction only for the direct dimension

"""
import nmrglue as ng
import numpy as np		
from base import dialog
import sys, os
		
def lindriftcomp(dic, data, start_phase, end_phase):

    taq = 1 / dic['acqus']['SW_h'] * (data.shape[-1] - 1)
    taq = np.linspace(0, taq, data.shape[-1])

    compdata = np.zeros(data.shape, dtype=data.dtype)
    for i, phase in enumerate(np.linspace(start_phase, end_phase, data.shape[0])):
        compdata[i] = data[i] * np.exp(1j * 2 * np.pi * phase * taq)

    return compdata


def main():
	
	_, folder, expno, procno= sys.argv
	
	oexpno = expno + "00"
	iexpno, oexpno, start, end, write_pdata = dialog(
    header="Linear Drift Correction",
    info="Correct Liner Drift in Time Domain Data",
    labels=[
        "EXPNO of the dataset to correct",
        "EXPNO of the output dataset",
        "Start Shift",
        "Delta Shift (Start - End)",        
        "Write Processed data?",
    ],
    types=["e", "e", "e", "e", "e"],
    values=[expno, oexpno, 0, 0, 0],
    comments=["", "", "", "", ""],
)
	
	start, end, pdata = float(start), float(end), bool(int(write_pdata))
	
	pdata = bool(int(pdata))
	fullpath = os.path.join(folder, iexpno)
	outpath = os.path.join(fullpath, str(oexpno))
	
	dic, data = ng.bruker.read(fullpath)
	compdata = lindriftcomp(dic, data, start_phase=start, end_phase=end)
	ng.bruker.write(f"{outpath}", dic, compdata, write_procs=pdata, pdata_folder=pdata, overwrite=True)
	
	
if __name__ == "__main__":
	main()
	
