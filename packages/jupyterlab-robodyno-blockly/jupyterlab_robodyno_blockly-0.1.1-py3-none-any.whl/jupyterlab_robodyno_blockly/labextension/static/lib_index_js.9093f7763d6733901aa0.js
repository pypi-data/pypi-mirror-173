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
    var code = 'Motor(can, 0x' + motor_id + ', ' + motor_type + ' )';
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
//# sourceMappingURL=lib_index_js.9093f7763d6733901aa0.js.map