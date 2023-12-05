# For Two Stl File visualisation

import vtk
def stl_file_visualisation(file1, file2):
    # First STL file
    reader1 = vtk.vtkSTLReader()
    reader1.SetFileName(file1)
    mapper1 = vtk.vtkPolyDataMapper()
    mapper1.SetInputConnection(reader1.GetOutputPort())
    actor1 = vtk.vtkActor()
    actor1.SetMapper(mapper1)

    # Second STL file
    reader2 = vtk.vtkSTLReader()
    reader2.SetFileName(file2)
    mapper2 = vtk.vtkPolyDataMapper()
    mapper2.SetInputConnection(reader2.GetOutputPort())
    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)

    # Create two renderers and position them side by side
    renderer1 = vtk.vtkRenderer()
    renderer2 = vtk.vtkRenderer()

    renderer1.SetViewport(0.0, 0.0, 0.5, 1.0)  # Left half of the window
    renderer2.SetViewport(0.5, 0.0, 1.0, 1.0)  # Right half of the window

    renderer1.AddActor(actor1)
    renderer2.AddActor(actor2)

    # Set background color for each renderer
    renderer1.SetBackground(1, 1, 1)  # Background color for the first renderer
    renderer2.SetBackground(1, 1, 1)  # Background color for the second renderer

    # Create a render window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer1)
    renderWindow.AddRenderer(renderer2)

    # Set up render window interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    renderWindowInteractor.Start()



stl_file_visualisation("./stl/Ikarus_55_felirat.stl", "./stl/Ikarus_66_felirat.stl")




















