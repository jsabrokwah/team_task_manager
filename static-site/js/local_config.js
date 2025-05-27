// Local configuration file for the Task Management System frontend
// Use this for local development testing

const config = {
    // Local API endpoint
    apiBaseUrl: 'http://127.0.0.1:5000/',
    
    // Authentication endpoints
    authEndpoints: {
        login: 'login',
        logout: 'logout',
        refresh: 'refresh',
        signup: 'signup'
    },
    
    // Task endpoints
    taskEndpoints: {
        create: 'tasks',
        list: 'tasks',
        userTasks: 'tasks/me',
        tasksByStatus: 'tasks/status/',
        userTasksByStatus: 'tasks/me/status/'
    },
    
    // User endpoints
    userEndpoints: {
        create: 'user/create',
        update: 'user/update/',
        delete: 'user/delete/',
        list: 'user/all',
        get: 'user/'
    },
    
    // Token storage keys
    tokenKeys: {
        accessToken: 'access_token',
        refreshToken: 'refresh_token'
    }
};