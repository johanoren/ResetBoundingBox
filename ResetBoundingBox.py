#Author-Johan Norén
#Description-Resets unconstrained width of textboxes in active sketch 

import adsk.core, adsk.fusion, traceback

_app = None
_ui  = None
_rowNumber = 0

_handlers = []

class ResetBoundingBoxInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self,args):
        try:
            pass
            # eventArgs= adsk.core.InputChangedEventArgs.cast(args)
            # inputs = eventArgs.inputs
            # cmdInput = eventArgs.input
            
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class ResetBoundingBoxExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self,args):
        try:
            cmd = args.firingEvent.sender
            inputs = cmd.commandInputs
            
            selectionInput = None
            
            for inputI in inputs:
                if inputI.id == 'sketchInput':
                    selectionInput = inputI

            sketches = []
            
            for i in range(0, selectionInput.selectionCount):
                selection = selectionInput.selection(i)
                selectedObj = selection.entity
                if type(selectedObj) is adsk.fusion.Sketch:
                   sketches.append(selectedObj)            
            
            for sketch in sketches:
                # Get textobjects in the sketch
                texts = sketch.sketchTexts
                noTexts = texts.count
                
                for i in range(noTexts):        
                    # Get the text item
                    textItem = texts.item(i)
                    # Save the old text
                    oldText = textItem.text
                    # Replace the text to reset the width of the box        
                    textItem.text = "X"
                    # change the text back to desired texts
                    textItem.text = oldText 
                
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class ResetBoundingBoxCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self,args):
        try:
            # Get command
            cmd = adsk.core.Command.cast(args.command)
            
            # Connect destroyed event handler
            onDestroy = ResetBoundingBoxDestroyHandler()
            cmd.destroy.add(onDestroy)
            _handlers.append(onDestroy)

            # Connect input changed event handler
            onInputChanged = ResetBoundingBoxInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            _handlers.append(onInputChanged)  
            
            # Connect execute handler
            onExecute = ResetBoundingBoxExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)
            
            inputs = cmd.commandInputs            
            
            # Add my select sketch thingy
            selectionInput = inputs.addSelectionInput('sketchInput','Select sketch','Select sketch to normalize text inside')
            selectionInput.setSelectionLimits(0)
            selectionInput.addSelectionFilter('Sketches')            
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class ResetBoundingBoxDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self,args):
        try:
            adsk.terminate()
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
def run(context):
    try:    
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui = _app.userInterface
        
        cmdDef = _ui.commandDefinitions.itemById('cmdResetBoundingBox')
        if not cmdDef:
            cmdDef = _ui.commandDefinitions.addButtonDefinition('cmdResetBoundingBox', 'Res Bounding Box', 'Resets bounding box for all text in sketch.')
    
        onCommandCreated = ResetBoundingBoxCreatedHandler()    
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)
        
        cmdDef.execute()    
        
        adsk.autoTerminate(False)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))