import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IBlocklyRegistry } from 'jupyterlab-blockly';

import { BlocklyRobodyno  } from './robodyno_python_generators';

/**
 * Initialization data for the jupyterlab-robodyno-blockly extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-robodyno-blockly:plugin',
  autoStart: true,
  requires: [IBlocklyRegistry],
  activate: (app: JupyterFrontEnd, blockly: IBlocklyRegistry) => {
    console.log('JupyterLab extension jupyterlab-robodyno-blockly is activated!');

    //Registering the new toolbox containing all Robodyno blocks.
    blockly.registerToolbox('robodyno', BlocklyRobodyno.Toolbox);

  }
};

export default plugin;


