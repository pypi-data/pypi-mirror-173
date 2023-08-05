"use strict";
(self["webpackChunkjupyterlab_robodyno_blockly"] = self["webpackChunkjupyterlab_robodyno_blockly"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var jupyterlab_blockly__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jupyterlab-blockly */ "webpack/sharing/consume/default/jupyterlab-blockly/jupyterlab-blockly");
/* harmony import */ var jupyterlab_blockly__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jupyterlab_blockly__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _robodyno_python_generators__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./robodyno_python_generators */ "./lib/robodyno_python_generators.js");


/**
 * Initialization data for the jupyterlab-robodyno-blockly extension.
 */
const plugin = {
    id: 'jupyterlab-robodyno-blockly:plugin',
    autoStart: true,
    requires: [jupyterlab_blockly__WEBPACK_IMPORTED_MODULE_0__.IBlocklyRegistry],
    activate: (app, blockly) => {
        console.log('JupyterLab extension jupyterlab-robodyno-blockly is activated!');
        //Registering the new toolbox containing all Robodyno blocks.
        blockly.registerToolbox('robodyno', _robodyno_python_generators__WEBPACK_IMPORTED_MODULE_1__.BlocklyRobodyno.Toolbox);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/robodyno_python_generators.js":
/*!*******************************************!*\
  !*** ./lib/robodyno_python_generators.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyRobodyno": () => (/* binding */ BlocklyRobodyno)
/* harmony export */ });
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! blockly/python */ "./node_modules/blockly/python.js");
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(blockly_python__WEBPACK_IMPORTED_MODULE_1__);


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
blockly__WEBPACK_IMPORTED_MODULE_0__.Blocks.robodyno_init_connect = {
    init: function () {
        this.appendDummyInput().appendField('start robodyno');
        this.appendDummyInput()
            .appendField(new blockly__WEBPACK_IMPORTED_MODULE_0__.FieldDropdown([
            ['motor', 'Motor'],
            ['robot', 'robots']
        ]), 'ROBODYNO_INIT_MODE');
        this.setInputsInline(true);
        this.setPreviousStatement(false, null);
        this.setNextStatement(true, null);
        this.setColour(function_color);
        this.setTooltip('Init Robodyno and can');
        this.setHelpUrl('https://pypi.org/project/robodyno/');
    }
};
blockly__WEBPACK_IMPORTED_MODULE_0__.Blocks.robodyno_motor_connect = {
    init: function () {
        this.appendDummyInput().appendField('robodyno motor');
        this.appendDummyInput()
            .appendField('id: 0x')
            .appendField(new blockly__WEBPACK_IMPORTED_MODULE_0__.FieldNumber(10, -Infinity, Infinity, 1), 'motor_id');
        this.appendDummyInput().appendField('type:');
        this.appendDummyInput()
            .appendField(new blockly__WEBPACK_IMPORTED_MODULE_0__.FieldDropdown([
            ['ROBODYNO_PRO_44', 'ROBODYNO_PRO_44'],
            ['ROBODYNO_PRO_12', 'ROBODYNO_PRO_12'],
            ['ROBODYNO_PRO_50', 'ROBODYNO_PRO_50'],
            ['ROBODYNO_PRO_100', 'ROBODYNO_PRO_100'],
        ]), 'ROBODYNO_MOTOR_TYPE');
        this.setInputsInline(true);
        this.setOutput(true, 'Boolean');
        this.setColour(function_color);
        this.setTooltip('add Robodyno motor object');
        this.setHelpUrl('https://pypi.org/project/robodyno/');
    }
};
blockly__WEBPACK_IMPORTED_MODULE_0__.Blocks.robodyno_motor_state = {
    init: function () {
        this.appendDummyInput().appendField('robodyno');
        this.appendValueInput('MOTOR_NAME').setCheck('VALUE');
        this.appendDummyInput().appendField('motor');
        this.appendDummyInput()
            .appendField(new blockly__WEBPACK_IMPORTED_MODULE_0__.FieldDropdown([
            ['enable', 'enable'],
            ['disable', 'disable']
        ]), 'ROBODYNO_MOTOR_STATE');
        this.setInputsInline(true);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(function_color);
        this.setTooltip('Robodyno motor enable or disable');
        this.setHelpUrl('https://pypi.org/project/robodyno/');
    }
};
blockly__WEBPACK_IMPORTED_MODULE_0__.Blocks.set_robodyno_motor = {
    init: function () {
        this.appendDummyInput().appendField('set ');
        this.appendValueInput('MOTOR_NAME').setCheck('VALUE');
        this.appendDummyInput().appendField('motor');
        this.appendDummyInput()
            .appendField(new blockly__WEBPACK_IMPORTED_MODULE_0__.FieldDropdown([
            ['pos', 'pos'],
            ['vel', 'vel'],
            ['torque', 'torque'],
        ]), 'SET_ROBODYNO_MOTOR');
        this.appendDummyInput()
            .appendField('value ')
            .appendField(new blockly__WEBPACK_IMPORTED_MODULE_0__.FieldNumber(0, -Infinity, Infinity, 0.0001), 'set_motor_value');
        this.setInputsInline(true);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(function_color);
        this.setTooltip('Set Robodyno motor pos or vel or torque');
        this.setHelpUrl('https://pypi.org/project/robodyno/');
    }
};
(blockly_python__WEBPACK_IMPORTED_MODULE_1___default().robodyno_init_connect) = function (block) {
    let branch = blockly_python__WEBPACK_IMPORTED_MODULE_1___default().statementToCode(block);
    var dropdown_init_mode = block.getFieldValue('ROBODYNO_INIT_MODE');
    var code = 'can = CanBus()\n' + branch;
    if (dropdown_init_mode == 'robots') {
        code = 'from robodyno.robots.six_dof_collaborative_robot import SixDoFCollabRobot\n' + code;
    }
    return code;
};
blockly__WEBPACK_IMPORTED_MODULE_0__.Blocks.robodyno_init_connect.toplevel_init = `
from robodyno.components import Motor
from robodyno.interfaces import CanBus
`;
(blockly_python__WEBPACK_IMPORTED_MODULE_1___default().robodyno_motor_connect) = function (block) {
    var motor_id = block.getFieldValue('motor_id');
    var motor_type = block.getFieldValue('ROBODYNO_MOTOR_TYPE');
    var code = 'Motor(can, 0x' + motor_id + ', "' + motor_type + '" )';
    return [code, (blockly_python__WEBPACK_IMPORTED_MODULE_1___default().ORDER_NONE)];
};
(blockly_python__WEBPACK_IMPORTED_MODULE_1___default().robodyno_motor_state) = function (block) {
    var motor_name = motor_name;
    motor_name = blockly_python__WEBPACK_IMPORTED_MODULE_1___default().valueToCode(block, 'MOTOR_NAME', (blockly_python__WEBPACK_IMPORTED_MODULE_1___default().ORDER_ATOMIC));
    var motor_state = block.getFieldValue('ROBODYNO_MOTOR_STATE');
    var code = motor_name + '.' + motor_state + '()\n';
    return code;
};
(blockly_python__WEBPACK_IMPORTED_MODULE_1___default().set_robodyno_motor) = function (block) {
    var motor_name = motor_name;
    motor_name = blockly_python__WEBPACK_IMPORTED_MODULE_1___default().valueToCode(block, 'MOTOR_NAME', (blockly_python__WEBPACK_IMPORTED_MODULE_1___default().ORDER_ATOMIC));
    var motor_value = block.getFieldValue('set_motor_value');
    var set_motor = block.getFieldValue('SET_ROBODYNO_MOTOR');
    var code = motor_name + '.set_' + set_motor + '(' + motor_value + ')';
    return code;
};
const TOOLBOX_ROBODYNO = {
    kind: 'categoryToolbox',
    contents: [
        {
            kind: 'category',
            name: 'Logic',
            colour: '210',
            contents: [
                {
                    kind: 'block',
                    type: 'controls_if'
                },
                {
                    kind: 'BLOCK',
                    type: 'logic_compare'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_operation"></block>',
                    type: 'logic_operation'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_negate"></block>',
                    type: 'logic_negate'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_boolean"></block>',
                    type: 'logic_boolean'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_null"></block>',
                    type: 'logic_null'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_ternary"></block>',
                    type: 'logic_ternary'
                }
            ]
        },
        {
            kind: 'category',
            name: 'Loops',
            colour: '120',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_repeat_ext">\n          <value name="TIMES">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'controls_repeat_ext'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_whileUntil"></block>',
                    type: 'controls_whileUntil'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_for">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n          <value name="BY">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'controls_for'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_forEach"></block>',
                    type: 'controls_forEach'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_flow_statements"></block>',
                    type: 'controls_flow_statements'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Math',
            colour: '230',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_number"></block>',
                    type: 'math_number'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_arithmetic">\n          <value name="A">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="B">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_arithmetic'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_single">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">9</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_single'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_trig">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">45</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_trig'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_constant"></block>',
                    type: 'math_constant'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_number_property">\n          <value name="NUMBER_TO_CHECK">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_number_property'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_change">\n          <value name="DELTA">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_change'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_round">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">3.1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_round'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_on_list"></block>',
                    type: 'math_on_list'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_modulo">\n          <value name="DIVIDEND">\n            <shadow type="math_number">\n              <field name="NUM">64</field>\n            </shadow>\n          </value>\n          <value name="DIVISOR">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_modulo'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_constrain">\n          <value name="VALUE">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="LOW">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="HIGH">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_constrain'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_random_int">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_random_int'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_random_float"></block>',
                    type: 'math_random_float'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Text',
            colour: '160',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text"></block>',
                    type: 'text'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_join"></block>',
                    type: 'text_join'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_append">\n          <value name="TEXT">\n            <shadow type="text"></shadow>\n          </value>\n        </block>',
                    type: 'text_append'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_length">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_length'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_isEmpty">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT"></field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_isEmpty'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n          <value name="FIND">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_indexOf'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_charAt">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
                    type: 'text_charAt'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_getSubstring">\n          <value name="STRING">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
                    type: 'text_getSubstring'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_changeCase">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_changeCase'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_trim">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_trim'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_print">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_print'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_prompt_ext">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_prompt_ext'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Lists',
            colour: '260',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_create_with">\n          <mutation items="0"></mutation>\n        </block>',
                    type: 'lists_create_with'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_create_with"></block>',
                    type: 'lists_create_with'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_repeat">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">5</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'lists_repeat'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_length"></block>',
                    type: 'lists_length'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_isEmpty"></block>',
                    type: 'lists_isEmpty'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_indexOf'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_getIndex">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_getIndex'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_setIndex">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_setIndex'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_getSublist">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_getSublist'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_split">\n          <value name="DELIM">\n            <shadow type="text">\n              <field name="TEXT">,</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'lists_split'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_sort"></block>',
                    type: 'lists_sort'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Color',
            colour: '20',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_picker"></block>',
                    type: 'colour_picker'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_random"></block>',
                    type: 'colour_random'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_rgb">\n          <value name="RED">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n          <value name="GREEN">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="BLUE">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'colour_rgb'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_blend">\n          <value name="COLOUR1">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#ff0000</field>\n            </shadow>\n          </value>\n          <value name="COLOUR2">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#3333ff</field>\n            </shadow>\n          </value>\n          <value name="RATIO">\n            <shadow type="math_number">\n              <field name="NUM">0.5</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'colour_blend'
                }
            ]
        },
        {
            kind: 'SEP'
        },
        {
            kind: 'CATEGORY',
            colour: '330',
            custom: 'VARIABLE',
            name: 'Variables'
        },
        {
            kind: 'CATEGORY',
            colour: '290',
            custom: 'PROCEDURE',
            name: 'Functions'
        },
        {
            kind: 'SEP'
        },
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
    Blocks: blockly__WEBPACK_IMPORTED_MODULE_0__.Blocks,
    Generator: (blockly_python__WEBPACK_IMPORTED_MODULE_1___default()),
    Toolbox: TOOLBOX_ROBODYNO
};
// export default [BlocklyNiryo, BlocklyNed];



/***/ })

}]);
//# sourceMappingURL=lib_index_js.6b0e7f3e193cc04d720c.js.map