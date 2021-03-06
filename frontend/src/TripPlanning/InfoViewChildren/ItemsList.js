import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import IconButton from '@material-ui/core/IconButton';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import ActivityElem from './ActivityElem'
import HostelElem from './HostelElem'

const gridStyle = theme => ({
    root: {
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-around',
        overflow: 'hidden',
        backgroundColor: theme.palette.background.paper,
    },
    gridList: {
        flexWrap: 'nowrap',
        // Promote the list into his own layer on Chrome. This cost memory but helps keeping high FPS.
        transform: 'translateZ(0)',
    },
    title: {
        color: theme.palette.primary.light,
    },
    titleBar: {
        background:
            'linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 70%, rgba(0,0,0,0) 100%)',
    },
});
function ActivitesList(props) {
    const { classes } = props;
    function items() {
        if (props.isActivity) {
            return props.elems.map(elem => (

                <ActivityElem
                    activity={elem}
                    activities={props.activities}
                    addActivity={props.addActivity.bind(this)}
                    removeActivity={props.removeActivity.bind(this)}

                />
            ));
        } else {
            return props.elems.map(elem => (
                <HostelElem
                    hostel={elem}
                    selectHostel={props.selectHostel.bind(this)}
                    selectedHostel={props.selectedHostel}
                />
            ));
        }
    }

    return (
        <div className={classes.root}>
            <GridList className={classes.gridList} cols={2.5}>
                {items()}
            </GridList>



        </div >
    );
}



export default withStyles(gridStyle)(ActivitesList);