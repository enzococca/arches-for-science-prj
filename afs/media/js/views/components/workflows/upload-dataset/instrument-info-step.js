define([
    'knockout',
    'utils/resource',
    'viewmodels/card',
], function(ko, resourceUtils) {
   
    function viewModel(params) {
        this.instrumentValue = ko.observable();
        this.procedureValue = ko.observable();
        this.parametersValue = ko.observable();
        this.nameValue = ko.observable();
        this.showName = ko.observable(false);
    }

    ko.components.register('instrument-info-step', {
        viewModel: viewModel,
        template: {
            require: 'text!templates/views/components/workflows/upload-dataset/instrument-info-step.htm'
        }
    });

    return viewModel;
});