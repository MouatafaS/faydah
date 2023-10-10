        // JavaScript code to handle menu toggle
        document.addEventListener('DOMContentLoaded', function () {
            const menuContainer = document.getElementById('menuContainer');
            const menu = document.getElementById('menu');
            const toggleButton = document.createElement('div');
            
            // افتراضيًا، نستخدم أيقونة القائمة
            toggleButton.innerHTML = '<i class="fa-solid fa-bars" style="color: #fff; font-size: 27px;"></i>';
            
            toggleButton.onclick = function () {
                menu.classList.toggle('active');
                
                // تغيير أيقونة الزر بناءً على حالة القائمة
                if (menu.classList.contains('active')) {
                    toggleButton.innerHTML = '<i class="fa-solid fa-times" style="color: #fff; font-size: 27px;"></i>';
                } else {
                    toggleButton.innerHTML = '<i class="fa-solid fa-bars" style="color: #fff; font-size: 27px;"></i>';
                }
            };
            
            menuContainer.appendChild(toggleButton);
        });
