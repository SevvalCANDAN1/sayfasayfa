function toggleRows(category){
    
    const rows = document.querySelectorAll('.' + category);

    rows.forEach(row => {
        //classList.contains() -> belirli css sınıfına sahip olup olmadığını kontrol eden method
        if (row.classList.contains('hidden-row')) {
            row.classList.remove('hidden-row'); 
            row.classList.add('visible-row');
        } else {
            row.classList.remove('visible-row'); 
            row.classList.add('hidden-row');
        }
    });
}


