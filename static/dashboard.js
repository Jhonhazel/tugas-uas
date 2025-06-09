document.addEventListener('DOMContentLoaded', function () {
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            } else {
                console.error('Lucide library tidak termuat dengan benar.');
            }

            const currentYearEl = document.getElementById('currentYear');
            if (currentYearEl) {
                currentYearEl.textContent = new Date().getFullYear();
            }

            const mobileMenuButton = document.getElementById('mobileMenuButton');
            const mobileSidebarEl = document.getElementById('mobileSidebar');
            const closeMobileMenuButton = document.getElementById('closeMobileMenuButton');

            if (mobileMenuButton && mobileSidebarEl && closeMobileMenuButton) {
                mobileMenuButton.addEventListener('click', () => {
                    mobileSidebarEl.classList.remove('hidden');
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                });

                closeMobileMenuButton.addEventListener('click', () => {
                    mobileSidebarEl.classList.add('hidden');
                });

                mobileSidebarEl.addEventListener('click', (event) => {
                    if (event.target === mobileSidebarEl) {
                        mobileSidebarEl.classList.add('hidden');
                    }
                });
            } else {
                console.error("Elemen menu mobile tidak ditemukan atau tidak lengkap.");
            }

            const profileDropdownButton = document.getElementById('profileDropdownButton');
            const profileDropdownMenu = document.getElementById('profileDropdownMenu');
            const mobileProfileDropdownButton = document.getElementById('mobileProfileDropdownButton');
            const mobileProfileDropdownMenu = document.getElementById('mobileProfileDropdownMenu');

            function setupDropdown(button, menu) {
                if (button && menu) {
                    button.addEventListener('click', function(event) {
                        event.stopPropagation();
                        const isHidden = menu.classList.contains('hidden');

                        if (isHidden) {
                            menu.classList.remove('hidden');
                            requestAnimationFrame(() => {
                                menu.classList.remove('opacity-0', 'scale-95', '-translate-y-2');
                                menu.classList.add('opacity-100', 'scale-100', 'translate-y-0');
                            });
                        } else {
                            menu.classList.remove('opacity-100', 'scale-100', 'translate-y-0');
                            menu.classList.add('opacity-0', 'scale-95', '-translate-y-2');
                            setTimeout(() => {
                                menu.classList.add('hidden');
                            }, 200);
                        }
                        if (typeof lucide !== 'undefined') {
                            lucide.createIcons();
                        }
                    });
                }
            }

            setupDropdown(profileDropdownButton, profileDropdownMenu);
            setupDropdown(mobileProfileDropdownButton, mobileProfileDropdownMenu);


            window.addEventListener('click', function(event) {
                [profileDropdownMenu, mobileProfileDropdownMenu].forEach(menu => {
                    if (menu && !menu.classList.contains('hidden')) {
                        const button = menu.id === 'profileDropdownMenu' ? profileDropdownButton : mobileProfileDropdownButton;
                        if (button && !button.contains(event.target) && !menu.contains(event.target)) {
                            menu.classList.remove('opacity-100', 'scale-100', 'translate-y-0');
                            menu.classList.add('opacity-0', 'scale-95', '-translate-y-2');
                            setTimeout(() => {
                                menu.classList.add('hidden');
                            }, 200);
                        }
                    }
                });
            });


            function initializeDragAndDrop(containerId) {
                const sidebarNav = document.getElementById(containerId);
                if (!sidebarNav) {
                    return;
                }
                let draggedItem = null;
                sidebarNav.addEventListener('dragstart', (e) => {
                    if (e.target.tagName === 'LI' && e.target.classList.contains('sidebar-menu-item')) {
                        draggedItem = e.target;
                        setTimeout(() => {
                            if(draggedItem) draggedItem.classList.add('dragging');
                        }, 0);
                        e.dataTransfer.setData('text/plain', e.target.innerText);
                        e.dataTransfer.effectAllowed = 'move';
                    } else {
                        e.preventDefault();
                    }
                });
                sidebarNav.addEventListener('dragend', (e) => {
                    if (draggedItem && e.target.classList.contains('sidebar-menu-item')) {
                         setTimeout(() => {
                            if(draggedItem) draggedItem.classList.remove('dragging');
                            draggedItem = null;
                        }, 0);
                    }
                    const items = sidebarNav.querySelectorAll('.sidebar-menu-item');
                    items.forEach(item => item.classList.remove('drag-over'));
                });
                sidebarNav.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    const targetItem = e.target.closest('.sidebar-menu-item');
                    if (targetItem && draggedItem && targetItem !== draggedItem) {
                        const items = sidebarNav.querySelectorAll('.sidebar-menu-item');
                        items.forEach(item => {
                            if (item !== targetItem) {
                                item.classList.remove('drag-over');
                            }
                        });
                        targetItem.classList.add('drag-over');
                        const rect = targetItem.getBoundingClientRect();
                        const nextSibling = getNextSibling(e.clientY, targetItem, rect);
                        if (nextSibling) {
                            sidebarNav.insertBefore(draggedItem, nextSibling);
                        } else {
                            sidebarNav.appendChild(draggedItem);
                        }
                    }
                });
                sidebarNav.addEventListener('drop', (e) => {
                    e.preventDefault();
                    const targetItem = e.target.closest('.sidebar-menu-item');
                    if (targetItem) {
                        targetItem.classList.remove('drag-over');
                    }
                });
                function getNextSibling(mouseY, element, rect) {
                    const halfway = rect.top + rect.height / 2;
                    if (mouseY < halfway) {
                        return element;
                    } else {
                        return element.nextElementSibling;
                    }
                }
            }
            initializeDragAndDrop('sidebarNav');
            initializeDragAndDrop('mobileSidebarNav');

            const geminiModal = document.getElementById('geminiResultModal');
            const geminiModalTitle = document.getElementById('geminiModalTitle');
            const geminiModalBody = document.getElementById('geminiModalBody');
            const closeGeminiModalButton = document.getElementById('closeGeminiModalButton');

            function showGeminiModal(title) {
                if (!geminiModal || !geminiModalTitle || !geminiModalBody) return;
                geminiModalTitle.textContent = title;
                geminiModalBody.innerHTML = '<p class="text-center py-4">Memuat hasil dari Gemini...</p>';
                geminiModal.classList.remove('hidden');
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }

            function closeGeminiModal() {
                 if (!geminiModal) return;
                geminiModal.classList.add('hidden');
            }

            if (closeGeminiModalButton) {
                closeGeminiModalButton.addEventListener('click', closeGeminiModal);
            }
            if (geminiModal) {
                geminiModal.addEventListener('click', function(event) {
                    if (event.target === geminiModal) {
                        closeGeminiModal();
                    }
                });
            }


            async function callGeminiAPI(prompt) {
                const apiKey = "";
                const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

                let chatHistory = [{ role: "user", parts: [{ text: prompt }] }];
                const payload = { contents: chatHistory };

                try {
                    const response = await fetch(apiUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        console.error('Error from Gemini API:', errorData);
                        return `Error: ${errorData.error?.message || response.statusText}`;
                    }

                    const result = await response.json();

                    if (result.candidates && result.candidates.length > 0 &&
                        result.candidates[0].content && result.candidates[0].content.parts &&
                        result.candidates[0].content.parts.length > 0) {
                        return result.candidates[0].content.parts[0].text;
                    } else {
                        console.error('Unexpected response structure from Gemini API:', result);
                        return "Tidak ada konten yang diterima dari Gemini.";
                    }
                } catch (error) {
                    console.error('Fetch error calling Gemini API:', error);
                    return "Terjadi kesalahan saat menghubungi layanan Gemini.";
                }
            }

            // --- Logika untuk Resize Sidebar ---
            const sidebar = document.getElementById('resizableSidebar');
            const resizeHandle = document.getElementById('resizeHandle');

            if (sidebar && resizeHandle) {
                let isResizing = false;
                let startX;
                let startWidth;
                const iconOnlyWidth = 80;
                const maxWidth = 320;

                function checkAndApplyCollapsedState(currentWidth) {
                    if (currentWidth <= iconOnlyWidth) {
                        if (!sidebar.classList.contains('sidebar-collapsed')) {
                            sidebar.classList.add('sidebar-collapsed');
                            if (typeof lucide !== 'undefined') lucide.createIcons();
                        }
                    } else {
                        if (sidebar.classList.contains('sidebar-collapsed')) {
                            sidebar.classList.remove('sidebar-collapsed');
                            if (typeof lucide !== 'undefined') lucide.createIcons();
                        }
                    }
                }

                const initialWidth = parseInt(document.defaultView.getComputedStyle(sidebar).width, 10);
                checkAndApplyCollapsedState(initialWidth);


                resizeHandle.addEventListener('mousedown', function(e) {
                    e.preventDefault();
                    isResizing = true;
                    startX = e.clientX;
                    startWidth = parseInt(document.defaultView.getComputedStyle(sidebar).width, 10);
                    document.body.style.cursor = 'col-resize';
                    document.body.style.userSelect = 'none';
                    sidebar.style.transition = 'none';
                });

                document.addEventListener('mousemove', function(e) {
                    if (!isResizing) return;

                    let newWidth = startWidth + (e.clientX - startX);

                    if (newWidth < iconOnlyWidth) {
                        newWidth = iconOnlyWidth;
                    } else if (newWidth > maxWidth) {
                        newWidth = maxWidth;
                    }
                    sidebar.style.width = newWidth + 'px';
                    checkAndApplyCollapsedState(newWidth);
                });

                document.addEventListener('mouseup', function(e) {
                    if (isResizing) {
                        isResizing = false;
                        document.body.style.cursor = 'default';
                        document.body.style.userSelect = 'auto';
                        sidebar.style.transition = 'width 0.1s ease-out';

                        const finalWidth = parseInt(document.defaultView.getComputedStyle(sidebar).width, 10);
                        checkAndApplyCollapsedState(finalWidth);
                    }
                });
            }


        });