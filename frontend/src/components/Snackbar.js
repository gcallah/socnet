import React, { Component } from "react";
import Snackbar from "@material-ui/core/Snackbar";
import MuiAlert from "@material-ui/lab/Alert";
import { makeStyles } from "@material-ui/core/styles";

class CustomSnackbar extends Component {

    state = {
        open: this.props.open,
        message: this.props.message,
    };

    useStyles = makeStyles((theme) => ({
        root: {
            width: "100%",
            "& > * + *": {
                marginTop: theme.spacing(2)
            }
        }
    }));

    handleClose = (event, reason) => {
        if (reason === "clickaway") {
            return;
        }
        this.setState({open: false});
    };

    render () {
        const { open, message }= this.state;
        return (
            <div >
                <Snackbar open={ open } autoHideDuration = {6000} onClose = { this.handleClose } >
                <MuiAlert elevation={6} variant="filled" onClose={ this.handleClose } severity="success" >
                    {message}
                </MuiAlert>
                </Snackbar>
            </div>
        );
    }

}

export default CustomSnackbar;
