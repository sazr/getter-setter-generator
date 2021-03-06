#-------------------------------------------------------------------------------
# Name:        Getter Setter View
# Purpose:     The View component of the applications' MVC architecture.
#
# Author:      Sam Zielke-Ryner
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import wx
import GenerationTypeChooser
from   os import getcwd
from   GetterSetterGlobal     import GS_GENERATE_CODE, GS_CLOSE, GS_FILE_DROP, GS_INPUT_CHANGE, GS_OUTPUT_CHANGE, GS_LANGUAGE_CHANGE, GS_FIND_VARIABLES, GS_UPDATE_VARIABLE
from   GetterSetterFileDrop   import FileDrop
from   GenerationTypeChooser  import *


# Attempt to import UltimateListCtrl
import sys, os

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import ultimatelistctrl
except ImportError: # if it's not there locally, try the wxPython lib.
    from wx.lib.agw import ultimatelistctrl as ULC





class GetterSetterView( wx.Frame ):

    ## Class Variables: ##

    # self.controller
    # self.parent
    # self.pos
    # self.dim

    # self.main_panel
    # self.main_sizer
    # self.generate_bt
    # self.input_eb
    # self.output_eb
    # self.language_cb
    # self.input_tf
    # self.output_tf
    # self.variable_lc


    ## Class Functions: ##

    def __init__( self, _parent, _controller, _pos, _dim, _layout ):
        """ Constructor: Define & initialise widgets """

        wx.Frame.__init__( self, _parent, -1, "Getter Setter Generator", pos = _pos, size = _dim )

        # Initialise variables
        self.controller = _controller
        self.parent     = _parent
        self.pos        = _pos
        self.dim        = _dim
        self.main_panel = wx.Panel( self, wx.ID_ANY, pos = (0,0), size = self.dim,
                                      style = wx.TAB_TRAVERSAL )

        self.main_sizer = wx.BoxSizer( _layout )


        # Create controls
        self.init_io_panel()
        self.init_button_panel_exx()


        self.main_panel.SetAutoLayout( True )
        self.main_panel.SetSizer( self.main_sizer )
        self.Centre()
        #self.main_panel.Layout()



    def init_io_panel( self ):
        """ Post: Initialise the input output widgets of the application """

        io_panel       = wx.Panel( self.main_panel, wx.ID_ANY )
        io_sizer       = wx.BoxSizer( wx.VERTICAL )
        self.input_eb  = wx.TextCtrl( io_panel, wx.ID_ANY, "Drag & Drop Files Here..",
                                      style = wx.TE_MULTILINE | wx.TE_WORDWRAP )
        self.output_eb = wx.TextCtrl( io_panel, wx.ID_ANY, "Getter & Setter functions will be displayed here",
                                      style = wx.TE_MULTILINE | wx.TE_WORDWRAP )
        input_dt       = FileDrop( self.input_eb, self )
        self.input_eb.SetDropTarget( input_dt )


        io_sizer.Add( (-1,10), 0 )
        io_sizer.Add( self.input_eb, 1, wx.EXPAND, 10 )
        io_sizer.Add( (10,10), 0 )
        io_sizer.Add( self.output_eb, 1, wx.EXPAND, 0 )


        io_panel.SetSizer( io_sizer )
        self.main_sizer.Add( io_panel, 2, wx.EXPAND | wx.ALL, 10 )



    def init_button_panel( self ):
        """ Post: Initialise the button menu of the application. Utilises
                  a vertical layout """

        language_cb_elements = ( 'C++', 'Java', 'Python' )

        control_panel    = wx.Panel( self.main_panel, wx.ID_ANY )
        control_sizer    = wx.BoxSizer( wx.VERTICAL )
        h_panel          = wx.Panel( control_panel, wx.ID_ANY )
        h_sizer          = wx.BoxSizer( wx.HORIZONTAL )


        control_panel.SetMinSize( wx.Size(250, 400) )


        find_var_bt      = wx.Button( h_panel, wx.ID_ANY, "Find Variables", size = (80,25) )
        self.generate_bt = wx.Button( h_panel, wx.ID_ANY, "Generate Getters|Setters", size = (-1,25) )
        h_sizer.Add( find_var_bt, 0, 0, 10 )
        h_sizer.Add( (10,-1), 0, 0, 10 )
        h_sizer.Add( self.generate_bt, 1, 0, 10 )
        h_panel.SetSizer( h_sizer )
        control_sizer.Add( (-1,10), 0 )
        control_sizer.Add( h_panel, 0, wx.EXPAND, 10 )
        control_sizer.Add( (-1,20), 0 )


        h_panel          = wx.Panel( control_panel, wx.ID_ANY )
        h_sizer          = wx.BoxSizer( wx.HORIZONTAL )
        self.language_cb = wx.ComboBox( h_panel, wx.ID_ANY, choices = language_cb_elements )
        h_sizer.Add( wx.StaticText( h_panel, wx.ID_ANY, "Language:" ), 1, wx.EXPAND, 10 )
        h_sizer.Add( self.language_cb, 1, wx.EXPAND, 10 )
        h_panel.SetSizer( h_sizer )
        control_sizer.Add( h_panel, 0, wx.EXPAND, 10 )
        control_sizer.Add( (-1,20), 0 )


        h_panel          = wx.Panel( control_panel, wx.ID_ANY )
        h_sizer          = wx.BoxSizer( wx.HORIZONTAL )
        choose_input_bt  = wx.Button( h_panel, wx.ID_ANY, "Browse Input", size = (-1,20) )
        self.input_tf    = wx.TextCtrl( h_panel, wx.ID_ANY, "", size = (-1,20) )
        h_sizer.Add( wx.StaticText( h_panel, wx.ID_ANY, "Input File:", size = (60,-1) ), 0, 0, 10 )
        h_sizer.Add( self.input_tf, 1, wx.EXPAND, 10 )
        h_sizer.Add( (5,-1), 0, wx.EXPAND )
        h_sizer.Add( choose_input_bt, 1, wx.EXPAND, 10 )
        h_panel.SetSizer( h_sizer )
        control_sizer.Add( h_panel, 0, wx.EXPAND, 10 )
        control_sizer.Add( (-1,20), 0 )


        h_panel          = wx.Panel( control_panel, wx.ID_ANY )
        h_sizer          = wx.BoxSizer( wx.HORIZONTAL )
        choose_output_bt = wx.Button( h_panel, wx.ID_ANY, "Browse Output", size = (-1,20) )
        self.output_tf   = wx.TextCtrl( h_panel, wx.ID_ANY, "", size = (-1,20) )
        h_sizer.Add( wx.StaticText( h_panel, wx.ID_ANY, "Output File:", size = (60,-1) ), 0, 0, 10 )
        h_sizer.Add( self.output_tf, 1, wx.EXPAND, 10 )
        h_sizer.Add( (5,-1), 0, wx.EXPAND )
        h_sizer.Add( choose_output_bt, 1, wx.EXPAND, 10 )
        h_panel.SetSizer( h_sizer )
        control_sizer.Add( h_panel, 0, wx.EXPAND, 10 )
        control_sizer.Add( (-1,20), 0 )


        #self.variable_lc = wx.ListCtrl( control_panel, wx.ID_ANY, style = wx.LC_LIST )
        self.variable_lc = ULC.UltimateListCtrl( control_panel, -1, agwStyle=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_VRULES | wx.LC_HRULES | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        #agwStyle = ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT )
        control_sizer.Add( (-1,10), 0 )
        control_sizer.Add( self.variable_lc, 1, wx.EXPAND, 10 )
        control_sizer.Add( (-1,10), 0 )


        h_panel          = wx.Panel( control_panel, wx.ID_ANY )
        h_sizer          = wx.BoxSizer( wx.HORIZONTAL )
        exit_bt          = wx.Button( h_panel, wx.ID_ANY, "Exit", size = (-1,20) )
        h_sizer.Add( (10,10), 1, wx.EXPAND )
        h_sizer.Add( exit_bt, 0, wx.EXPAND, 10 )
        h_panel.SetSizer( h_sizer )
        control_sizer.Add( h_panel, 0, wx.EXPAND, 10 )
        # control_sizer.Add( (-1,10), 0 )


        control_panel.SetSizer( control_sizer )
        self.main_sizer     .Add( control_panel, 0, wx.EXPAND | wx.ALL, 10 )
        self.main_sizer     .Add( (10,-1), 0, wx.EXPAND, 10 )


        # Add columns to ultimate list control
        self.variable_lc    .InsertColumn( 0, 'Variable Name' )
        self.variable_lc    .InsertColumn( 1, 'Data Type' )
        self.variable_lc    .InsertColumn( 2, 'Value' )
        self.variable_lc    .InsertColumn( 3, 'Wrapper' )
        self.variable_lc    .InsertColumn( 4, 'Type' )
        self.language_cb    .SetSelection( 0 )
        self.input_tf       .SetEditable( False )
        self.output_tf      .SetEditable( False )
        self.toggle_generate_bt( False )


        col_widths = ( 75, 57, 35, 50, 35 )
        for col in range( self.variable_lc.GetColumnCount() ):

            self.variable_lc    .SetColumnWidth( col, col_widths[ col ] )
            self.variable_lc    .SetColumnWidth( col, wx.LIST_AUTOSIZE_USEHEADER )



        #Bind controls to events
        find_var_bt         .Bind( wx.EVT_BUTTON, self.on_find_variables_command )
        exit_bt             .Bind( wx.EVT_BUTTON, self.on_close_command )
        choose_input_bt     .Bind( wx.EVT_BUTTON, self.on_choose_file_command )
        choose_output_bt    .Bind( wx.EVT_BUTTON, self.on_choose_file_command )
        self.generate_bt    .Bind( wx.EVT_BUTTON, self.on_generate_command )
        self.language_cb    .Bind( wx.EVT_COMBOBOX, self.on_language_change_command )



    def init_button_panel_ex( self ):
        """ Post: Initialise the button menu of the application. Utilises
                  a horizontal layout """

        language_cb_elements = ( 'C++', 'Java', 'Python' )

        control_panel = wx.Panel( self.main_panel, wx.ID_ANY )
        control_sizer = wx.BoxSizer( wx.HORIZONTAL )

        # Add button controls
        # button_box       = wx.StaticBox( control_panel, wx.ID_ANY )
        button_sizer     = wx.StaticBoxSizer( control_panel, wx.HORIZONTAL )
        find_var_bt      = wx.Button( control_panel, wx.ID_ANY, "Find Variables", size = (80,25) )
        self.generate_bt = wx.Button( control_panel, wx.ID_ANY, "Generate Getters|Setters", size = (-1,25) )
        button_sizer.Add( find_var_bt, 0, 0, 10 )
        button_sizer.Add( (10,-1), 0, 0, 10 )
        button_sizer.Add( self.generate_bt, 1, 0, 10 )
        # button_box.SetSizer( button_sizer )
        control_sizer.Add( (10,-1), 0 )
        control_sizer.Add( button_box, 0, wx.EXPAND, 10 )
        control_sizer.Add( (20,-1), 0 )


        # Add language attribute controls
        # attrib_box       = wx.StaticBox( control_panel, wx.ID_ANY )
        attrib_sizer     = wx.StaticBoxSizer( control_panel, wx.HORIZONTAL )
        self.language_cb = wx.ComboBox( control_panel, wx.ID_ANY, choices = language_cb_elements )
        attrib_sizer.Add( wx.StaticText( control_panel, wx.ID_ANY, "Language:" ), 1, wx.EXPAND, 10 )
        attrib_sizer.Add( self.language_cb, 1, wx.EXPAND, 10 )
        # attrib_box.SetSizer( attrib_sizer )
        control_sizer.Add( attrib_box, 0, wx.EXPAND, 10 )
        control_sizer.Add( (20,-1), 0 )


        # Add input/output controls
        file_box              = wx.StaticBox( control_panel, wx.ID_ANY )
        file_sizer            = wx.StaticBoxSizer( file_box, wx.VERTICAL )
        input_panel           = wx.Panel( file_box, wx.ID_ANY )
        input_sizer           = wx.BoxSizer( wx.HORIZONTAL )
        choose_input_bt       = wx.Button( input_panel, wx.ID_ANY, "Browse Input", size = (-1,20) )
        self.input_tf         = wx.TextCtrl( input_panel, wx.ID_ANY, "", size = (-1,20) )
        self.save_output_file = wx.Button( input_panel, wx.ID_ANY, "Save Output", size = (-1,20) )

        input_sizer.Add( wx.StaticText( input_panel, wx.ID_ANY, "Input File:", size = (60,-1) ), 0, 0, 10 )
        input_sizer.Add( self.input_tf, 0, 0, 10 )
        input_sizer.Add( choose_input_bt, 0, 0, 10 )
        input_panel.SetSizer( input_sizer )
        file_sizer.Add( input_panel, 0, 0, 10 )
        file_sizer.Add( self.save_output_file, 0, 0, 10 )
        # file_box.SetSizer( file_sizer )
        control_sizer.Add( file_box, 0, wx.EXPAND, 10 )
        control_sizer.Add( (10,-1), 0 )


        control_panel.SetSizer( control_sizer )
        self.main_sizer     .Add( control_panel, 0, wx.EXPAND | wx.ALL, 10 )


        # Add ULC
        self.variable_lc = ULC.UltimateListCtrl( self.main_panel, -1, agwStyle = ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        self.main_sizer.Add( (20,-1), 0 )
        self.main_sizer.Add( self.variable_lc, 1, wx.EXPAND, 10 )


        # Add exit button
        h_box            = wx.Panel( self.main_panel, wx.ID_ANY )
        h_sizer          = wx.BoxSizer( wx.HORIZONTAL )
        exit_bt          = wx.Button( h_box, wx.ID_ANY, "Exit", size = (-1,20) )
        h_sizer.Add( (300,20), 0, wx.EXPAND, 10 )
        h_sizer.Add(  exit_bt, 0, wx.EXPAND, 10 )
        h_box.SetSizer( h_sizer )
        self.main_sizer.Add( (10,-1), 0 )
        self.main_sizer.Add( h_box, 0, wx.EXPAND, 10 )


        # Add columns to ultimate list control
        self.variable_lc    .InsertColumn( 0, 'Variable Name' )
        self.variable_lc    .InsertColumn( 1, 'Data Type' )
        self.variable_lc    .InsertColumn( 2, 'Value' )
        self.variable_lc    .InsertColumn( 3, 'Wrapper' )
        self.variable_lc    .InsertColumn( 4, 'Type' )
        self.language_cb    .SetSelection( 0 )
        self.input_tf       .SetEditable( False )
        self.toggle_generate_bt( False )


        col_widths = ( 75, 57, 35, 50, 35 )
        for col in range( self.variable_lc.GetColumnCount() ):

            self.variable_lc    .SetColumnWidth( col, col_widths[ col ] )



        #Bind controls to events
        find_var_bt         .Bind( wx.EVT_BUTTON, self.on_find_variables_command )
        exit_bt             .Bind( wx.EVT_BUTTON, self.on_close_command )
        choose_input_bt     .Bind( wx.EVT_BUTTON, self.on_choose_file_command )
        self.save_output_file    .Bind( wx.EVT_BUTTON, self.on_choose_file_command )
        self.generate_bt    .Bind( wx.EVT_BUTTON, self.on_generate_command )
        self.language_cb    .Bind( wx.EVT_COMBOBOX, self.on_language_change_command )



    def init_button_panel_exx( self ):
        """ Post: Initialise the button menu of the application. Utilises
                  a horizontal layout """

        language_cb_elements = ( 'C++', 'Java', 'Python' )

        control_panel = wx.Panel( self.main_panel, wx.ID_ANY )
        control_sizer = wx.BoxSizer( wx.VERTICAL )

        # Add button controls
        h_box         = wx.Panel( control_panel )
        h_box_sizer   = wx.BoxSizer( wx.HORIZONTAL )
        find_var_bt      = wx.Button( h_box, wx.ID_ANY, "Find Variables", size = (80,25) )
        self.generate_bt = wx.Button( h_box, wx.ID_ANY, "Generate Getters|Setters", size = (-1,25) )
        h_box_sizer.Add( find_var_bt, 0, 0, 0 )
        h_box_sizer.Add( (10,-1), 0, 0, 0 )
        h_box_sizer.Add( self.generate_bt, 1, 0, 0 )

        self.language_cb = wx.ComboBox( h_box, wx.ID_ANY, choices = language_cb_elements )
        h_box_sizer.Add( (100,-1), 0, 0, 10 )
        h_box_sizer.Add( wx.StaticText( h_box, wx.ID_ANY, "Language:", size = (60,-1) ),0, 0, 10 )
        h_box_sizer.Add( self.language_cb, 1, wx.EXPAND, 10 )
        h_box.SetSizer( h_box_sizer )
        control_sizer.Add( h_box, 0, wx.EXPAND, 0 )
        control_sizer.Add( (-1,10), 0 )


        # Add input/output controls
        h_box         = wx.Panel( control_panel )
        h_box_sizer   = wx.BoxSizer( wx.HORIZONTAL )
        choose_input_bt       = wx.Button( h_box, wx.ID_ANY, "Browse Input", size = (-1,20) )
        self.input_tf         = wx.TextCtrl( h_box, wx.ID_ANY, "", size = (-1,20) )
        # self.save_output_file = wx.Button( h_box, wx.ID_ANY, "Save Output", size = (-1,20) )
        h_box_sizer.Add( (300,-1), 0, 0, 10 )
        h_box_sizer.Add( wx.StaticText( h_box, wx.ID_ANY, "Input File:", size = (60,-1) ), 0, 0, 10 )
        h_box_sizer.Add( self.input_tf, 1, 0, 10 )
        h_box_sizer.Add( (5,-1), 0, 0, 10 )
        h_box_sizer.Add( choose_input_bt, 1, 0, 10 )
        h_box.SetSizer( h_box_sizer )
        control_sizer.Add( h_box, 0, wx.EXPAND, 10 )
        control_sizer.Add( (-1,10), 0 )


        # Add ULC
        self.variable_lc = ULC.UltimateListCtrl( control_panel, -1, agwStyle = ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        control_sizer.Add( self.variable_lc, 1, wx.EXPAND, 0 )
        control_sizer.Add( (-1,8), 0 )


        # Add exit button
        h_box            = wx.Panel( control_panel, wx.ID_ANY )
        h_sizer          = wx.BoxSizer( wx.HORIZONTAL )
        exit_bt          = wx.Button( h_box, wx.ID_ANY, "Exit", size = (80,20) )
        h_sizer.Add( (590,-1), 1, wx.EXPAND, 10 )
        h_sizer.Add(  exit_bt, 0, 0, 10 )
        h_box.SetSizer( h_sizer )
        control_sizer.Add( h_box, 0, wx.EXPAND, 5 )

        control_panel.SetSizer( control_sizer )
        self.main_sizer     .Add( control_panel, 1, wx.EXPAND | wx.ALL, 10)


        # Add columns to ultimate list control
        self.variable_lc    .InsertColumn( 0, 'Variable Name' )
        self.variable_lc    .InsertColumn( 1, 'Data Type' )
        self.variable_lc    .InsertColumn( 2, 'Value' )
        self.variable_lc    .InsertColumn( 3, 'Wrapper' )
        self.variable_lc    .InsertColumn( 4, 'Type' )
        self.language_cb    .SetSelection( 0 )
        self.input_tf       .SetEditable( False )
        self.toggle_generate_bt( False )


        col_widths = ( 75, 57, 35, 50, 35 )
        for col in range( self.variable_lc.GetColumnCount() ):

            self.variable_lc    .SetColumnWidth( col, col_widths[ col ] )



        #Bind controls to events
        find_var_bt         .Bind( wx.EVT_BUTTON, self.on_find_variables_command )
        exit_bt             .Bind( wx.EVT_BUTTON, self.on_close_command )
        choose_input_bt     .Bind( wx.EVT_BUTTON, self.on_choose_file_command )
        # self.save_output_file    .Bind( wx.EVT_BUTTON, self.on_choose_file_command )
        self.generate_bt    .Bind( wx.EVT_BUTTON, self.on_generate_command )
        self.language_cb    .Bind( wx.EVT_COMBOBOX, self.on_language_change_command )



    def show_error_dialog( self, error_str ):
        """ Post: Display an application message/error in a message dialog """

        dial = wx.MessageDialog( self, error_str, "Error:",
                                 wx.OK | wx.NO_DEFAULT | wx.ICON_ERROR )

        ret = dial.ShowModal()



    def toggle_generate_bt( self, enable_button ):
        """ Post: Enable or disable the button responsible for sending the
                  generate Getter Setter code message """

        if ( enable_button == True ):

            self.generate_bt.Enable()

        else:

            self.generate_bt.Disable()



    def on_close_command( self, event ):
        """ Post: Inform the Controller component that the user wants to close
                  the application """

        """
        dial = wx.MessageDialog( None, 'Are you sure to quit?', 'Question',
                                 wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION )

        ret = dial.ShowModal()

        if ret == wx.ID_YES:
            self.Destroy()
        else:
            event.Veto()
        """

        self.controller.window_proc( GS_CLOSE, None )



    def on_generate_command( self, event ):
        """ Post: Send message to controller that the user wants us to
                  generate Setter Getter code """

        self.controller.window_proc( GS_GENERATE_CODE, None )



    def on_find_variables_command( self, event ):
        """ Post: Send 'search source code for variables' message to
                  controller along with the source code """

        input_content = self.input_eb.GetValue()

        self.controller.window_proc( GS_FIND_VARIABLES, input_content )



    def on_language_change_command( self, event ):
        """ Post: Notify controller that the user has selected a new
                  programming language to generate the Getter Setter
                  code in """

        # Get combobox selected langauage & pass as WPARAM
        sel_lang = self.language_cb.GetValue()

        self.controller.window_proc( GS_LANGUAGE_CHANGE, sel_lang )



    def notify_file_drop( self, file_name ):
        """ Post: Notify controller that the source code (that we search
                  for variables) is different """

        self.controller.window_proc( GS_INPUT_CHANGE, file_name )



    def on_choose_file_command( self, event ):
        """ Post: Open a file chooser dialog to allow user to open or save
                  a file """

        src       = event.GetEventObject()
        bt_type   = src.GetLabel()

        if bt_type == "Browse Input":
            dialog_flags = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST

        else:
            dialog_flags = wx.FD_SAVE | wx.FD_FILE_MUST_EXIST


        file_chooser = wx.FileDialog( self, "Choose a file", getcwd(), "",
                                      style = (wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) )

        sel_action = file_chooser.ShowModal()


        if sel_action != wx.ID_CANCEL :

            file_name = file_chooser.GetPath()


            if bt_type == "Browse Input":

                self.controller.window_proc( GS_INPUT_CHANGE, file_name )

            else:  # elif bt_type == "Browse Output"  or bt_type == "Save Output":

                self.controller.window_proc( GS_OUTPUT_CHANGE, file_name )



    def on_generation_type_change( self, event ):
        """ Post: Notify controller that the user has changed a variables
                  code generation type. A variables code generation type
                  indicates whether we should generate only Getter functions,
                  only Setter functions or both for a specific variable  """

        src          = event.GetEventObject()
        sel_variable = src.variable_index
        sel_gen_type = src.GetStringSelection()

        self.controller.window_proc( GS_UPDATE_VARIABLE, (sel_variable, sel_gen_type) )



    def set_input_content( self, input_data ):
        """ Post: Display the name of the programming file & the source code
                  that file contains """

        self.input_tf.Clear()
        self.input_eb.Clear()
        self.input_tf.WriteText( input_data[0] )  # input file name
        self.input_eb.WriteText( input_data[1] )  # input file contents



    def set_output_content( self, output_content ):
        """ Post: Display the Getter Setter code we have generated for
                  variables """

        self.output_eb.Clear()
        self.output_eb.WriteText( output_content )



    def set_output_name( self, output_file_name ):
        """ Post: Display the name of the file we are saving the automatically
                  generated Getter Setter code to """

        self.output_tf.Clear()
        self.output_tf.WriteText( output_file_name )



    def delete_variable_list_elements( self ):
        """ Post: Delete all cells (that document variables we have identified
                  in the source code) from the UltimateListControl widget """

        itemCount = self.variable_lc.GetItemCount()

        for item in range( itemCount ):

            self.variable_lc.DeleteItem( 0 )


        # OR
        # self.variable_lc.DeleteAllItems()
        # OR
        # self.variable_lc.ClearAll()



    def display_variables( self, var_list ):
        """ Post: Display (all variables we have identified in the source
                  code) in the UlitmateListControl widget"""

        variable_index = 0
        self.delete_variable_list_elements()


        for variable in var_list:

            row = self.variable_lc.GetItemCount()

            row_items = ( variable.var_name,
                          variable.data_type,
                          str( variable.var_value ),
                          variable.wrapper_name )

            self.variable_lc.InsertStringItem( row, "" )
            column_index = 0

            for item in row_items:

                self.variable_lc.SetItemOverFlow( row, column_index, False )
                self.variable_lc.SetStringItem( row, column_index, item )
                column_index += 1


            # Put in Gen chooser
            gen_type_chooser = GenerationTypeChooser( self, self.variable_lc, -1, "None", variable_index )
            self.variable_lc.SetItemWindow( row, 4, gen_type_chooser )
            self.variable_lc.SetItemOverFlow( row, 3, False )

            variable_index += 1


