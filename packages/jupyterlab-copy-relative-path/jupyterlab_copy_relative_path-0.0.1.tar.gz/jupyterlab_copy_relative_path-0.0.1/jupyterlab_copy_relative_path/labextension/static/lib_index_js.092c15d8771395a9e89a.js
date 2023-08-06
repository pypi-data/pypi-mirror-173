"use strict";
(self["webpackChunkjupyterlab_copy_relative_path"] = self["webpackChunkjupyterlab_copy_relative_path"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
const application_1 = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
const filebrowser_1 = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
const docmanager_1 = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const ui_components_1 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
const extension = {
    id: 'context-menu',
    autoStart: true,
    requires: [filebrowser_1.IFileBrowserFactory, docmanager_1.IDocumentManager, application_1.ILabShell],
    activate: (app, factory, docManager, labShell) => {
        app.commands.addCommand('filebrowser:copy-relative-path', {
            label: 'Copy Relative Path',
            caption: 'Copy path relative to the active notebook.',
            icon: ui_components_1.fileIcon.bindprops({ stylesheet: 'menuItem' }),
            execute: () => {
                const widget = factory.tracker.currentWidget;
                if (!widget) {
                    return;
                }
                const item = widget.selectedItems().next();
                if (!item) {
                    return;
                }
                if (!labShell.currentWidget) {
                    return;
                }
                console.debug('labShell.currentWidget:', labShell.currentWidget);
                const context = docManager.contextForWidget(labShell.currentWidget);
                if (!context) {
                    return;
                }
                console.debug(`context.path: ${context.path}`);
                const relativePath = utils_1.getRelativePath(item.path, context.path);
                apputils_1.Clipboard.copyToSystem(relativePath);
                console.debug(`Copied relative path to clipboard: ${relativePath}`);
            },
            isVisible: () => !!factory.tracker.currentWidget &&
                !!factory.tracker.currentWidget.selectedItems().next() &&
                !!labShell.currentWidget &&
                !!docManager.contextForWidget(labShell.currentWidget),
        });
    },
};
exports["default"] = extension;


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.getRelativePath = void 0;
// Get relative path of target with respect to reference
const getRelativePath = (target, reference) => {
    const xs = target.split('/');
    const ys = reference.split('/').slice(0, -1);
    const n = Math.min(xs.length, ys.length);
    let count = 0;
    for (let i = 0; i < n; i++) {
        if (xs[i] === ys[i]) {
            count++;
        }
        else {
            break;
        }
    }
    const numUps = ys.length - count;
    const zs = [...Array(numUps).fill('..'), ...xs.slice(count)];
    return zs.join('/');
};
exports.getRelativePath = getRelativePath;


/***/ })

}]);
//# sourceMappingURL=lib_index_js.092c15d8771395a9e89a.js.map