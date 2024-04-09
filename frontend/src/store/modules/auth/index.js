import mutations from './mutations';
import actions from './actions';
import getters from './getters';

export default {
    namespace: true,
    state() {
        return {
            name: 'Pallavi Pandey',
        };
    },  
    mutations,
    actions,
    getters,
};