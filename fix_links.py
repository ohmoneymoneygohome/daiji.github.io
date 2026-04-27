content = open('index.html', 'r', encoding='utf-8').read()

# 找到有问题的那一行，然后用正确的内容替换整个导航栏
old_nav = '''                <div class="hidden md:flex space-x-8">
                    <a href="#home" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">首页</a>
                    <a href="#generations" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">代际档案</a>
                    <a href="#insights" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">维度洞察</a>
                    <a href="#methodology" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">前沿方法论</a>
                    <a href="#contributors" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">代际理论贡献者</a>
                    <a href="#library" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">代际图书馆</a>
                    <a<a href="podcast.html" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">小憩</a>
                </div>'''

new_nav = '''                <div class="hidden md:flex space-x-8">
                    <a href="#home" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">首页</a>
                    <a href="#generations" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">代际档案</a>
                    <a href="#insights" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">维度洞察</a>
                    <a href="#methodology" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">前沿方法论</a>
                    <a href="#contributors" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">代际理论贡献者</a>
                    <a href="#library" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">代际图书馆</a>
                    <a href="podcast.html" class="text-gray-700 hover:text-primary transition-colors px-2 py-1 rounded-md hover:bg-primary/5">小憩</a>
                </div>'''

content = content.replace(old_nav, new_nav)

# 修复移动端导航
content = content.replace('<a href="about.html" class="block text-gray-700 hover:text-primary px-3 py-2 rounded-md hover:bg-primary/5 transition-colors">小憩</a>', '<a href="podcast.html" class="block text-gray-700 hover:text-primary px-3 py-2 rounded-md hover:bg-primary/5 transition-colors">小憩</a>')

# 修复 banner 中的链接
old_banner_link = '<a href="about.html" class="px-6 py-3 bg-transparent text-white border border-white rounded-lg hover:bg-white/10 transition-colors">'
new_banner_link = '<a href="podcast.html" class="px-6 py-3 bg-transparent text-white border border-white rounded-lg hover:bg-white/10 transition-colors">'
content = content.replace(old_banner_link, new_banner_link)

open('index.html', 'w', encoding='utf-8').write(content)
print('修复完成！')
