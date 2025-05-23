


export const styles = {

    profileContent : {
        flexWrap: 'wrap',
        padding: '1.0rem',
        marginTop: '1.5rem',
        display: 'flex',
        borderRadius: '12px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        backgroundColor: '#f0f8ff',
        color: '#1e90ff',
        border: '1px solid #1e90ff',
        flexDirection: 'column'
    },
    modalOverlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000,
    },
    modalContent: {
        backgroundColor: '#f0f8ff',
        padding: '2rem',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
        maxWidth: '90%',
    },
    modalMessage: {
        fontSize: '1.7rem',
        color: '#1e90ff',
        marginBottom: '1rem',
    },
    modalButton: {
        flexShrink : 0,
        fontSize: '1.2rem',
        padding: '0.5rem 3rem',
        borderRadius: '12px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        backgroundColor: '#1e90ff',
    },
    deleteProfileContainer : {
        display: 'flex', 
        justifyContent: 'flex-end',
        width: '100%' 
    },
    deleteProfileButton : {
        flexShrink: 0,
        fontSize: '1.2rem',
        background: 'red', 
        padding: '0.5rem 1.2rem',
        borderRadius: '20px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    paramsContainer: {
        marginTop : '1.5rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '1.5rem',
        width: '100%',
        marginBottom : '2rem'
    },
    paramRow: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%',
        gap: '2rem',
    },
    textRow : {
        color: '#1e90ff',
        fontSize: '1.5rem',
        lex: '0 0 60%',
        textAlign: 'left',
    },
    dateButton: {
        padding: '0.3rem 1.5rem',
        fontSize: '1.2rem',
        backgroundColor : '#f0f8ff',
        border: '2px solid #1e90ff',
        borderRadius: '10px',
        cursor: 'pointer',
    },
    paramControl: {
        display: 'flex',
        justifyContent: 'flex-end',
    },
    modalButtons: {
        display: 'flex',
        justifyContent: 'center',
        gap: '0.5rem'
    },
    cancelButton: {
        flexShrink: 0,
        fontSize: '1.2rem',
        background: 'red', 
        padding: '0.5rem 1.2rem',
        borderRadius: '20px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    applyButton: {
        flexShrink: 0,
        fontSize: '1.2rem',
        background: '#4CAF50', 
        padding: '0.5rem 1.2rem',
        borderRadius: '20px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    label: {
        fontSize: '1.7rem',
        color: '#1e90ff',
        marginBottom: '0.5rem',
        padding: '0.8rem 1.2rem',
    },
    numberInput: {
        width: '3rem',
        padding: '0.4rem 0.8rem',
        fontSize: '1.2rem',
        backgroundColor : '#f0f8ff',
        border: '2px solid #1e90ff',
        borderRadius: '10px',
        maxWidth: '150px',
        marginLeft: '1rem'
    },
    intervalsContainer: {
        flexWrap: 'wrap',
        display: 'flex'
    },
    addButton: {
        flexShrink: 0,
        fontSize: '1.2rem',
        display: 'inline-block',
        margin: '0.5rem',
        padding: '0.8rem 1.2rem',
        borderRadius: '20px',
        backgroundColor: '#f0f8ff',
        color: '#1e90ff',
        border: '2px solid #1e90ff',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    intervalButton: {
        flexShrink: 0,
        fontSize: '1.2rem',
        display: 'inline-block',
        margin: '0.5rem',
        padding: '0.8rem 1.2rem',
        borderRadius: '20px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease'
    },
    saveChangesButton: {
        position: 'fixed',
        bottom: '2rem',
        left: '50%',
        transform: 'translateX(-50%)',
        backgroundColor: '#4CAF50',
        color: 'white',
        padding: '1rem 2rem',
        borderRadius: '25px',
        border : '2px solid #e0e0e0',
        cursor: 'pointer',
        fontSize: '1.5rem',
        boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
        transition: 'all 0.2s ease'
  }
};
