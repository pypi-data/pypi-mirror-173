

import * as Blockly from 'blockly';
import BlocklyPy from 'blockly/python';
import * as zh from 'blockly/msg/zh-hans'

var robodyno_one_color = '#3D4D9A';

// Interface color
var logic_color = '#00876d';
var loop_color = '#49a563';
var math_color = '#5769a1';
var list_color = '#765da1';
var variable_color = '#ad5a7e';
// var function_color = '#844D84';
var function_color = '210';

var movement_color = '#4f87c0';
var io_color = '#a200d8';
var tool_color = '#bf964b';
var utility_color = '#bead76';
var vision_color = '#3B1344';
var conveyor_color = '#00838f';
var sound_color = '#C9A3A2';
var frames_color = '#546e7a';
var led_color = '#105E1D';
var trajectory_color = '#9370DB';

// Color object for vision
//TODO Should be in a class
const g_color_values = {
  COLOR_RED: 'RED',
  COLOR_GREEN: 'GREEN',
  COLOR_BLUE: 'BLUE',
  COLOR_ANY: 'ANY'
};

// Shape object for vision
//TODO Should be in a class
const g_shape_values = {
  SHAPE_SQUARE: 'SQUARE',
  SHAPE_CIRCLE: 'CIRCLE',
  SHAPE_ANY: 'ANY'
};

/*
 *  Blocks definition
 */

// Connection

Blockly.Blocks['robodyno_init_connect'] = {
  init: function () {
    this.appendDummyInput().appendField('start robodyno');
    this.appendDummyInput()
      .appendField(
        new Blockly.FieldDropdown([
          ['motor', 'Motor'],
          ['robot', 'robots']
        ]),
        'ROBODYNO_INIT_MODE'
      )
    this.setInputsInline(true);
    this.setPreviousStatement(false, null);
    this.setNextStatement(true, null);
    this.setColour(function_color);
    this.setTooltip('Init Robodyno and can');
    this.setHelpUrl('https://pypi.org/project/robodyno/');
  }
};

Blockly.Blocks['robodyno_motor_connect'] = {
  init: function () {
    this.appendDummyInput().appendField('robodyno motor');
    this.appendDummyInput()
      .appendField('id: 0x')
      .appendField(
        new Blockly.FieldNumber(10, -Infinity, Infinity, 1),
        'motor_id'
      )
    this.appendDummyInput().appendField('type:');
    this.appendDummyInput()
      .appendField(
        new Blockly.FieldDropdown([
          ['ROBODYNO_PRO_44', 'ROBODYNO_PRO_44'],
          ['ROBODYNO_PRO_12', 'ROBODYNO_PRO_12'],
          ['ROBODYNO_PRO_50', 'ROBODYNO_PRO_50'],
          ['ROBODYNO_PRO_100', 'ROBODYNO_PRO_100'],
        ]),
        'ROBODYNO_MOTOR_TYPE'
      )
    this.setInputsInline(true);
    this.setOutput(true, 'Boolean');
    this.setColour(function_color);
    this.setTooltip('add Robodyno motor object');
    this.setHelpUrl('https://pypi.org/project/robodyno/');
  }
};



Blockly.Blocks['robodyno_motor_state'] = {
  init: function () {
    this.appendDummyInput().appendField('robodyno');
    this.appendValueInput('MOTOR_NAME').setCheck('VALUE')
    this.appendDummyInput().appendField('motor');
    this.appendDummyInput()
      .appendField(
        new Blockly.FieldDropdown([
          ['enable', 'enable'],
          ['disable', 'disable']
        ]),
        'ROBODYNO_MOTOR_STATE'
      )
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(function_color);
    this.setTooltip('Robodyno motor enable or disable');
    this.setHelpUrl('https://pypi.org/project/robodyno/');
  }
};

Blockly.Blocks['set_robodyno_motor'] = {
  init: function () {
    this.appendDummyInput().appendField('set ');
    this.appendValueInput('MOTOR_NAME').setCheck('VALUE')
    this.appendDummyInput().appendField('motor');
    this.appendDummyInput()
      .appendField(
        new Blockly.FieldDropdown([
          ['pos', 'pos'],
          ['vel', 'vel'],
          ['torque', 'torque'],
        ]),
        'SET_ROBODYNO_MOTOR'
      );
    this.appendDummyInput()
    .appendField('value ')
    .appendField(
      new Blockly.FieldNumber(0, -Infinity, Infinity, 0.0001),
      'set_motor_value'
    );
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(function_color);
    this.setTooltip('Set Robodyno motor pos or vel or torque');
    this.setHelpUrl('https://pypi.org/project/robodyno/');
  }
};



BlocklyPy['robodyno_init_connect'] = function (block) {

  let branch = BlocklyPy.statementToCode(block);
  var dropdown_init_mode = block.getFieldValue('ROBODYNO_INIT_MODE');
  var code = 'can = CanBus()\n' + branch;
  if (dropdown_init_mode == 'robots'){
    code = 'from robodyno.robots.six_dof_collaborative_robot import SixDoFCollabRobot\n' + code;
  }

  return code;
};

Blockly.Blocks['robodyno_init_connect'].toplevel_init = `
from robodyno.components import Motor
from robodyno.interfaces import CanBus
`;

BlocklyPy['robodyno_motor_connect'] = function (block) {

  var motor_id = block.getFieldValue('motor_id');
  var motor_type = block.getFieldValue('ROBODYNO_MOTOR_TYPE');
  var code = 'Motor(can, 0x' + motor_id + ', ' + motor_type + ' )';

  return [code, BlocklyPy.ORDER_NONE];
};


BlocklyPy['robodyno_motor_state'] = function (block) {

  var motor_name = motor_name;
  motor_name = BlocklyPy.valueToCode(
    block,
    'MOTOR_NAME',
    BlocklyPy.ORDER_ATOMIC
  );
  var motor_state = block.getFieldValue('ROBODYNO_MOTOR_STATE');
  var code = motor_name + '.' + motor_state + '()\n';

  return code;
};

BlocklyPy['set_robodyno_motor'] = function (block) {

  var motor_name = motor_name;
  motor_name = BlocklyPy.valueToCode(
    block,
    'MOTOR_NAME',
    BlocklyPy.ORDER_ATOMIC
  );
  var motor_value = block.getFieldValue('set_motor_value');
  var set_motor = block.getFieldValue('SET_ROBODYNO_MOTOR');
  var code = motor_name + '.set_' + set_motor + '(' + motor_value + ')';

  return code;
};

const TOOLBOX_ROBODYNO = {
  kind: 'categoryToolbox',
  contents: [
    {
      kind: 'CATEGORY',
      colour: function_color,
      name: 'Motor Connect',
      contents: [
        {
          kind: 'BLOCK',
          type: 'robodyno_init_connect'
        },
        {
          kind: 'BLOCK',
          type: 'robodyno_motor_connect'
        },
        {
          kind: 'BLOCK',
          type: 'robodyno_motor_state'
        },
        {
          kind: 'BLOCK',
          type: 'set_robodyno_motor'
        },
      ]
    },
    // {
    //   kind: 'CATEGORY',
    //   colour: movement_color,
    //   name: 'SixDoFCollabRobot',
    //   contents: [

    //   ]
    // },
  ]
};

const BlocklyRobodyno = {
  Blocks: Blockly.Blocks,
  Generator: BlocklyPy,
  Toolbox: TOOLBOX_ROBODYNO
};


// export default [BlocklyNiryo, BlocklyNed];
export { BlocklyRobodyno };
