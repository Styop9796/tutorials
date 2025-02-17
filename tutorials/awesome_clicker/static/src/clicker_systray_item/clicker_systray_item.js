/** @odoo-module */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../clicker_hook";


export class ClickerSystray extends Component {
    static template = "awesome_clicker.ClickerSystray";
    static props = {};

    setup() {
        this.action = useService("action");
        this.clicker = useClicker();
    }
    
    increment() {
        this.state.counter += 9;
        }



        openClientAction() {
            this.action.doAction({
                type: "ir.actions.client",
                tag: "awesome_clicker.client_action",
                target: "new",
                name: "Clicker Game"
            });
        }

}

export const systrayItem = {
    Component: ClickerSystray,
};

registry.category("systray").add("awesome_clicker.ClickerSystray", systrayItem, { sequence: 1000 });
