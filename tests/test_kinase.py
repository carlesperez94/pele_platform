import pytest
import os
import pele_platform.constants.constants as cs
import pele_platform.main as main
import shutil

test_path = os.path.join(cs.DIR, "Examples")


BIAS_ARGS = [os.path.join(test_path, "bias/input.yaml")]
OUT_IN_ARGS = [os.path.join(test_path, "out_in/input.yaml")]
INDUCED_ARGS = [os.path.join(test_path, "induced_fit/input.yaml")]
GLOBAL_ARGS = [os.path.join(test_path, "global/input.yaml")]
EXIT_ARGS = [os.path.join(test_path, "exit/input.yaml")]
EXITSOFT_ARGS = [os.path.join(test_path, "exit_soft/input.yaml")]
WATER_ARGS = [os.path.join(test_path, "water/input_bs.yaml")]
WATERLIG_ARGS = [os.path.join(test_path, "water/input_lig.yaml")]
RESTART_ARGS = [os.path.join(test_path, "restart/input.yaml")]
MSM_ARGS = [os.path.join(test_path, "Msm/input.yaml")]
MAE_ARGS = [os.path.join(test_path, "induced_fit/input_mae.yaml")]
FLAGS_ARGS = [os.path.join(test_path, "flags/input.yaml")]

ADAPTIVE_VALUES = ["PR_1A28_xray_-_minimized_processed.pdb", "STR", '"outputPath": "output_sim"',
    '"processors" : 3', '"peleSteps" : 1,', '"iterations" : 1,', '"runEquilibration" : true,',
    '"equilibrationLength" : 11,', '"seed": 3000', '"useSrun": true', 
    '"values" : [1, 2, 3],', '"conditions": [0.1, 0.2, 0.3]', '"epsilon": 0.3', 
    '"metricColumnInReport" : 3,', '"metricColumnInReport" : 3,', '"type" : "epsilon"',
    'exitContinuous']

PELE_VALUES = ['"reportPath": "$OUTPUT_PATH/rep",', '"trajectoryPath": "$OUTPUT_PATH/traj.xtc"',
                'OBC', '"anmFrequency" : 3,', '"sideChainPredictionFrequency" : 3,',
                '"minimizationFrequency" : 3,', '"temperature": 3000,',
                '{ "type": "constrainAtomToPosition", "springConstant": 3, "equilibriumDistance": 0.0, "constrainThisAtom": "A:151:_CA_" },',
                '"radius": 3000',
                '"fixedCenter": [30,30,30]',
                'tests/native.pdb"',
                '"atoms": { "ids":["A:2:_HB3"]}',
                '"atoms": { "ids":["A:2:_HB2"]}',
                'simulationLogPath'
              ]



def test_induced(ext_args=INDUCED_ARGS):
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.set_software_to_use(arguments)
    main.Launcher(arguments).launch()

def test_global(ext_args=GLOBAL_ARGS):
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.set_software_to_use(arguments)
    main.Launcher(arguments).launch()

def test_exit(ext_args=EXIT_ARGS):
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.set_software_to_use(arguments)
    main.Launcher(arguments).launch()

def test_exitsoft(ext_args=EXITSOFT_ARGS):
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.set_software_to_use(arguments)
    main.Launcher(arguments).launch()

def test_water(ext_args=WATER_ARGS):
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.set_software_to_use(arguments)
    main.Launcher(arguments).launch()

def test_water_lig(ext_args=WATERLIG_ARGS):
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.set_software_to_use(arguments)
    main.Launcher(arguments).launch()

def test_bias(ext_args=BIAS_ARGS):
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.set_software_to_use(arguments)
    main.Launcher(arguments).launch()

def test_restart(ext_args=RESTART_ARGS):
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.set_software_to_use(arguments)
    main.Launcher(arguments).launch()

#def test_msm(ext_args=MSM_ARGS):
#    arguments = main.parseargs_yaml(ext_args)
#    arguments = main.YamlParser(arguments.input_file)
#    main.set_software_to_use(arguments)
#    main.Launcher(arguments).launch()

def test_mae(ext_args=MAE_ARGS):
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.set_software_to_use(arguments)
    main.Launcher(arguments).launch()

def test_flags(ext_args=FLAGS_ARGS):
    errors = []
    arguments = main.parseargs_yaml(ext_args)
    arguments = main.YamlParser(arguments.input_file)
    main.set_software_to_use(arguments)
    main.Launcher(arguments).launch()
    folder = arguments.folder
    if not os.path.exists(os.path.join(folder, "DataLocal/LigandRotamerLibs/LIG.rot.assign")) or not os.path.exists(os.path.join(folder, "DataLocal/LigandRotamerLibs/MG.rot.assign")):
        errors.append("External rotamer flag not working")
    if not os.path.exists(os.path.join(folder, "DataLocal/Templates/OPLS2005/HeteroAtoms/ligz")) or not os.path.exists(os.path.join(folder, "DataLocal/Templates/OPLS2005/HeteroAtoms/mgz")):
        errors.append("External templates flag not working")
    if os.path.exists(os.path.join(folder, arguments.output)):
        errors.append("Debug flag not working")
    errors = check_file(folder, "adaptive.conf", ADAPTIVE_VALUES, errors)
    errors = check_file(folder, "pele.conf", PELE_VALUES, errors)
    errors = check_file(folder, "DataLocal/LigandRotamerLibs/STR.rot.assign", "60", errors)
    assert not errors


def check_file(folder, filename, values, errors):
   filename = os.path.join(folder, filename)
   with open(filename, "r") as f:
      lines = f.readlines()
      for value in values:
          if value not in "".join(lines):
              errors.append(value) 
   return errors
