// Configuration file for the Task Management System frontend
// Replace these values with the actual endpoints from your deployment

const config = {
    // API endpoint from CloudFormation output
    apiBaseUrl: 'https://your-api-id.execute-api.your-region.amazonaws.com/',
    
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