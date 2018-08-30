import subprocess
import MSM_PELE.Utilities.Helpers.pele_env as pele
import MSM_PELE.constants as cs
import MSM_PELE.Utilities.Helpers.system_prep as sp
import MSM_PELE.Utilities.PPP.mut_prep4pele as ppp
import MSM_PELE.Utilities.PlopRotTemp.main as plop
import MSM_PELE.Utilities.Helpers.missing_residues as mr
import MSM_PELE.Utilities.Helpers.simulation as ad




def run_adaptive(args):
    # Build folders and logging
    env = pele.EnviroBuilder.build_env(args)

    if args.restart == "all":

        # Build System
        env.logger.info("Checking {} system for Pele".format(args.residue))
        syst = sp.SystemBuilder.build_system(args.system, args.mae_lig, args.residue, env.pele_dir)

        # Prepare System
        system_fix, missing_residues, gaps, metals, protein_constraints = ppp.main(syst.system, env.pele_dir, charge_terminals=args.charge_ter, no_gaps_ter=args.gaps_ter)
        env.logger.info(cs.SYSTEM.format(system_fix, missing_residues, gaps, metals))

        # Parametrize Ligand
        if not env.external_template and not env.external_rotamers:
            env.logger.info("Creating template for residue {}".format(args.residue))
            plop.parametrize_miss_residues(args, env, syst)
            env.logger.info("Template {}z created".format(args.residue.lower()))
        else:
            cmd_to_move_template = "cp {} {}".format(env.external_template,  env.template_folder)
            subprocess.call(cmd_to_move_template.split())
            cmd_to_move_rotamer_file = "cp {} {}".format(env.external_rotamers,  env.rotamers_folder)
            subprocess.call(cmd_to_move_rotamer_file.split())



        # Parametrize missing residues
        for res, __, _ in missing_residues:
            if res != args.residue:
                env.logger.info("Creating template for residue {}".format(res))
                mr.create_template(system_fix, res, env.pele_dir, args.forcefield)
                env.logger.info("Template {}z created".format(res))

        # Fill in Simulation Templates
        adaptive = ad.SimulationBuilder.simulation_handler(env, protein_constraints) 
        adaptive.run()
        
    return env
