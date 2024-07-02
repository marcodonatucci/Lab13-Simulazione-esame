import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        years = self._model.getYears()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        self._view.update_page()

    def fillDDShape(self, e):
        self._view.ddshape.options.clear()
        shapes = self._model.getShapes(self._view.ddyear.value)
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        if self._view.ddyear.value is None or self._view.ddshape.value is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci una forma e un anno!", color='red'))
            self._view.update_page()
            return
        flag = self._model.buildGraph(self._view.ddyear.value, self._view.ddshape.value)
        if flag:
            result = self._model.getGraphDetails()
            for r in result:
                self._view.txt_result.controls.append(ft.Text(r))
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(ft.Text("Errore nella creazione del grafo!", color='red'))
            self._view.update_page()
            return

    def handle_path(self, e):
        self._view.txtOut2.controls.clear()
        if len(self._model.graph.nodes) == 0:
            self._view.txtOut2.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        componenti = self._model.getPath()
        if componenti:
            self._view.txtOut2.controls.append(ft.Text(f"Distanza totale del percorso: {self._model._bestdTot}"))
            for c in self._model.getPathDetails():
                self._view.txtOut2.controls.append(ft.Text(f"{c[0]} --> {c[1]}: {c[2]}, distanza: {c[3]}km"))
            self._view.update_page()
            return
        else:
            self._view.txtOut2.controls.append(ft.Text("Errore durante l'analisi dei componenti!", color='red'))
            self._view.update_page()
            return
